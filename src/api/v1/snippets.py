from fastapi import FastAPI, Depends, HTTPException, APIRouter
from sqlalchemy.ext.asyncio import AsyncSession
from schemas.snippet import SnippetCreate, SnippetResponse, SnippetUpdate
from services.crud_snippet import create_snippet, get_snippet, get_snippets, update_snippet, delete_snippet, get_snippet_by_shared_url_from_db
from db.db import db_dependency
from auth.auth import has_role



# Создаем экземпляр APIRouter
snippets_router = APIRouter(prefix="/snippets", tags=['snippets'])


@snippets_router.post("/", response_model=SnippetResponse, dependencies=[Depends(has_role(["user"]))])
async def create_new_snippet(snippet: SnippetCreate, db: db_dependency):
    """Создать новый сниппет"""
    return await create_snippet(db, snippet)


@snippets_router.get("/{snippet_id}", response_model=SnippetResponse, dependencies=[Depends(has_role(["user"]))])
async def read_snippet(snippet_id: int, db: db_dependency):
    """Получить сниппет по ID"""
    snippet = await get_snippet(db, snippet_id)
    if not snippet:
        raise HTTPException(status_code=404, detail="Snippet not found")
    return snippet


@snippets_router.get("/", response_model=list[SnippetResponse], dependencies=[Depends(has_role(["user"]))])
async def read_snippets(db: db_dependency, skip: int = 0, limit: int = 10):
    """Получить список сниппетов с пагинацией"""
    return await get_snippets(db, skip, limit)


@snippets_router.put("/{snippet_id}", response_model=SnippetResponse, dependencies=[Depends(has_role(["user"]))])
async def update_existing_snippet(
        snippet_id: int, snippet: SnippetUpdate, db: db_dependency):
    """Обновить существующий сниппет"""
    updated_snippet = await update_snippet(db, snippet_id, snippet)
    if not updated_snippet:
        raise HTTPException(status_code=404, detail="Snippet not found")
    return updated_snippet


@snippets_router.delete("/{snippet_id}", dependencies=[Depends(has_role(["user"]))])
async def delete_existing_snippet(snippet_id: int, db: db_dependency):
    """Удалить существующий сниппет"""
    snippet = await delete_snippet(db, snippet_id)
    if not snippet:
        raise HTTPException(status_code=404, detail="Snippet not found")
    return {"message": "Snippet deleted successfully"}





@snippets_router.get("/shared/{shared_url}", response_model=SnippetResponse)
async def get_snippet_by_shared_url(shared_url: str, db: db_dependency):
    """Получить сниппет по уникальной ссылке"""
    snippet = await get_snippet_by_shared_url_from_db(db, shared_url)
    if not snippet:
        raise HTTPException(status_code=404, detail="Snippet not found")
    return snippet
