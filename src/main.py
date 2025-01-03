import uvicorn
from fastapi import APIRouter, HTTPException, Depends, FastAPI, Request
from src.core.config import uvicorn_options
from src.core.logger import LOGGING_CONFIG
from src.models.model import MyGetFuncResponseSchema, User, UserResponse
from src.api import api_router
from sqlalchemy import text
from db.db import db_dependency
import logging.config
import logging.handlers
import atexit
from contextlib import asynccontextmanager
from typing import AsyncContextManager
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter()

logger = logging.getLogger("root")

# экземпляр роутера - метод - путь
@router.get("/path", response_model=MyGetFuncResponseSchema)
def my_get_func():
    return {
        "app_name": "MyAPP",
        "number_of_months": 12,
        "pi": 3.14
    }


@router.post("/path", response_model=UserResponse)
async def my_post_func(user_id: int, db: AsyncSession = Depends(db_dependency)):
    query = await db.execute(select(User).filter(User.id == user_id))
    user = query.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return UserResponse.from_orm(user)

@router.put("/path")
def my_put_func():
    pass


@router.delete("/path")
def my_delete_func():
    pass


@router.get('/ping')
async def ping(db: db_dependency):
    try:
        await db.execute(text("SELECT 1"))
        return True
    except Exception:
        return False


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncContextManager[None]:
    logging.config.dictConfig(LOGGING_CONFIG)
    # получаем обработчик очереди из корневого логгера
    queue_handler = logging.getHandlerByName("queue_handler")
    try:
        # если логгер есть
        if queue_handler is not None:
            # запускаем слушатель очереди
            queue_handler.listener.start()
            # регистрируем функцию, которая будет вызвана при завершении работы программы
            atexit.register(queue_handler.listener.stop)
        yield
    finally:
        # в случае ошибки выключаем слушатель
        if queue_handler is not None:
            queue_handler.listener.stop()


app = FastAPI(
    lifespan=lifespan,
    docs_url="/api/openapi"
)

app.include_router(router)
app.include_router(api_router)


@app.middleware("http")
async def error_middleware(request: Request, call_next):
    try:
        return await call_next(request)
    except HTTPException as exc:
        return JSONResponse(
            status_code=exc.status_code,
            content={"message": exc.detail}
        )
    except Exception as e:
        logger.error(f"{request.url} | Error in application: {e}")
        return JSONResponse(
            status_code=500,
            content={"message": "Internal server error"}
        )


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Error occurred: {request.url} - {str(exc)}")
    return JSONResponse(
        status_code=500,
        content={"message": "Internal server error"}
    )

if __name__ == '__main__':
    # print для отображения настроек в терминале при локальной разработке
    print(uvicorn_options)
    uvicorn.run(
        'main:app',
        **uvicorn_options
    )
