import multiprocessing
from pydantic_settings import BaseSettings
from pydantic import PostgresDsn
from pydantic_core import MultiHostUrl
import logging

class AppSettings(BaseSettings):
    app_port: int = 8000
    app_host: str = 'localhost'
    reload: bool = True
    cpu_count: int | None = None
    postgres_dsn: PostgresDsn = MultiHostUrl(
        'postgresql+asyncpg://postgres:admin@127.0.0.1/dbapi')
    jwt_secret: str = "your_super_secret"  # Добавьте эту переменную
    algorithm: str = "HS256"  # И эту переменную

    class Config:
        _env_file = ".env"
        _extra = 'allow'


app_settings = AppSettings()

# набор опций для запуска сервера
uvicorn_options = {
    "host": app_settings.app_host,
    "port": app_settings.app_port,
    "workers": app_settings.cpu_count or multiprocessing.cpu_count(),
    "reload": app_settings.reload
}
