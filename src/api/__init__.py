from fastapi import APIRouter


from api.v1.auth import auth_router

from api.v1.user import user_router


api_router = APIRouter()


api_router.include_router(user_router)
api_router.include_router(auth_router)