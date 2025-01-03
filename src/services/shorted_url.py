from sqlalchemy.future import select

from db.db import db_dependency
from models import ShortedUrl


async def get_url_by_id(db: db_dependency, url_id: int):
	result = await db.execute(select(ShortedUrl).filter(ShortedUrl.id == url_id))
	return result.scalars().first()


async def get_url_by_shorted_url(db: db_dependency, shorted_url: str):
	result = await db.execute(select(ShortedUrl).filter(ShortedUrl.shorted_url == shorted_url))
	return result.scalars().first()


async def get_urls(db: db_dependency, skip: int = 0, limit: int = 10):
	result = await db.execute(select(ShortedUrl).offset(skip).limit(limit))
	return result.scalars().all()


async def create_url(db: db_dependency, origin: str, shorted_url: str):
	db_url = ShortedUrl(origin=origin, shorted_url=shorted_url)
	db.add(db_url)
	await db.commit()
	await db.refresh(db_url)
	return db_url

async def update_url(db: db_dependency, url_id: int, origin: str, shorted_url: str):
	db_url = await get_url_by_id(db, url_id)
	if db_url:
    	db_url.origin = origin
    	db_url.shorted_url = shorted_url
    	await db.commit()
    	await db.refresh(db_url)
	return db_url

async def delete_url(db: db_dependency, url_id: int):
	db_url = await get_url_by_id(db, url_id)
	if db_url:
    	await db.delete(db_url)
    	await db.commit()
	return db_url