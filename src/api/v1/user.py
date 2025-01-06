import httpx
from fastapi import APIRouter, Depends, HTTPException, status
from schemas.user import UserRegisterSchema, UserLoginSchema
from db.db import db_dependency
from auth.auth import reg_user, authenticate_user, create_access_token,has_role  # Импортируем нужные функции
from fastapi import BackgroundTasks

# Создаем APIRouter с префиксом "/user" и тегом 'user' для отображения в документации
user_router = APIRouter(prefix="/user", tags=['user'])


@user_router.get("/{user_id}", dependencies=[Depends(has_role(["admin"]))])
async def get_user(user_id: int, db: db_dependency):
    # Выполняем запрос к базе данных
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalars().first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return {
        "id": user.id,
        "name": user.name,
        "email": user.email,
    }


@user_router.post("/register")
async def register_user(user_data: UserRegisterSchema, db: db_dependency):
    try:
        return await reg_user(user_data=user_data, db=db)
    except Exception as ex:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f"Аn error has occurred: {ex}")


@user_router.post("/login")
async def login_for_access_token(db: db_dependency,
                                 login_data: UserLoginSchema):
    user = await authenticate_user(login_data, db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(
        data={"sub": {"email": user.email}}
    )
    return {"access_token": access_token, "token_type": "bearer"}


@user_router.post("/send-notification/{email}", dependencies=[Depends(has_role(["admin"]))])
async def send_notification(email: str, background_tasks: BackgroundTasks):
    background_tasks.add_task(write_notification, email, message="some notification")
    return {"message": "Notification sent in the background"}
