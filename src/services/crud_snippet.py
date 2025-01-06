from sqlalchemy.future import select
from db.db import db_dependency
from models.model import Snippet
from schemas.snippet import SnippetCreate, SnippetUpdate
import uuid

async def create_snippet(db: db_dependency, snippet: SnippetCreate) -> Snippet:
    # Если сниппет публичный, генерируем уникальную ссылку
    shared_url = str(uuid.uuid4()) if not snippet.is_private else None
    db_snippet = Snippet(**snippet.dict(), shared_url=shared_url)
    db.add(db_snippet)
    await db.commit()
    await db.refresh(db_snippet)
    return db_snippet

async def get_snippet(db: db_dependency, snippet_id: int):
    result = await db.execute(select(Snippet).filter(Snippet.id == snippet_id))
    return result.scalars().first()

async def get_snippets(db: db_dependency, skip: int = 0, limit: int = 10):
    result = await db.execute(select(Snippet).offset(skip).limit(limit))
    return result.scalars().all()


async def update_snippet(db: db_dependency, snippet_id: int, snippet: SnippetUpdate) -> Snippet:

    db_snippet = await get_snippet(db, snippet_id)

    if db_snippet:
        # Если изменяется параметр is_private и сниппет становится публичным
        if snippet.is_private != db_snippet.is_private:
            if not snippet.is_private:  # Если становится публичным
                db_snippet.shared_url = str(uuid.uuid4())  # Генерируем новую уникальную ссылку
            else:
                db_snippet.shared_url = None  # Если становится приватным, убираем ссылку

        # Обновление остальных данных
        for key, value in snippet.dict(exclude_unset=True).items():
            setattr(db_snippet, key, value)

        # Сохранение изменений в базе данных
        await db.commit()
        await db.refresh(db_snippet)

    return db_snippet

async def delete_snippet(db: db_dependency, snippet_id: int):
    db_snippet = await get_snippet(db, snippet_id)
    if db_snippet:
        await db.delete(db_snippet)
        await db.commit()
    return db_snippet

async def get_snippet_by_shared_url_from_db(db: db_dependency, shared_url: str):
    """Запрос для получения сниппета по уникальной ссылке"""
    result = await db.execute(select(Snippet).filter(Snippet.shared_url == shared_url))
    snippet = result.scalars().first()
    return snippet