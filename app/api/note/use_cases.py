import datetime
import math
from typing import Annotated

from fastapi import Depends, HTTPException

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import async_sessionmaker

from db import get_session
from api.base.base_schemas import PaginationMetaResponse, PaginationParams
from models.note import Note, NoteSchema
from .schemas import CreateNoteRequest, UpdateNoteRequest

AsyncSession = Annotated[async_sessionmaker, Depends(get_session)]

class CreateNote:
    def __init__(self, session: AsyncSession) -> None:
        self.async_session = session

    async def execute(
            self,
            user_id: int,
            request: CreateNoteRequest
        ) -> NoteSchema:
        async with self.async_session.begin() as session:
            note = await session.execute(
                select(Note).where(Note.created_by == user_id)
            )
            note = note.scalars().first()

            note = Note()
            note.title = request.title
            note.content = request.content
            note.created_at = datetime.datetime.utcnow()
            note.updated_at = datetime.datetime.utcnow()
            note.created_by = user_id
            note.updated_by = user_id

            session.add(note)
            await session.flush()

            return NoteSchema.from_orm(note)

class ReadAllNote:
    def __init__(self, session: AsyncSession) -> None:
        self.async_session = session

    async def execute(
        self,
        user_id: int,
        page_params: PaginationParams,
        filter_user: bool,
        include_deleted: bool,
    ) -> (list[NoteSchema], PaginationMetaResponse):
        async with self.async_session() as session:
            total_item = (
                select(func.count())
                .select_from(Note)
            )

            query = (
                select(Note)
                .offset((page_params.page - 1) * page_params.item_per_page)
                .limit(page_params.item_per_page)
            )

            if filter_user:
                total_item = total_item.filter(Note.created_by == user_id)
                query = query.filter(Note.created_by == user_id)

            if not include_deleted:
                total_item = total_item.filter(Note.deleted_at == None)
                query = query.filter(Note.deleted_at == None)

            total_item = await session.execute(total_item)
            total_item = total_item.scalar()

            paginated_query = await session.execute(query)
            paginated_query = paginated_query.scalars().all()

            notes = [NoteSchema.from_orm(p) for p in paginated_query]

            meta = PaginationMetaResponse(
                total_item=total_item,
                page=page_params.page,
                item_per_page=page_params.item_per_page,
                total_page=math.ceil(total_item / page_params.item_per_page),
            )

            return notes, meta

class ReadNote:
    def __init__(self, session: AsyncSession) -> None:
        self.async_session = session

    async def execute(
            self,
            user_id: int,
            note_id: int
        ) -> NoteSchema:
        async with self.async_session() as session:
            note = await session.execute(
                select(Note).where(
                    (Note.created_by == user_id) &
                    (Note.note_id == note_id) &
                    (Note.deleted_at == None)
                )
            )
            note = note.scalars().first()
            if not note:
                raise HTTPException(status_code=404)

            return NoteSchema.from_orm(note)

class UpdateNote:
    def __init__(self, session: AsyncSession) -> None:
        self.async_session = session

    async def execute(
            self,
            user_id: int,
            note_id: int,
            request: UpdateNoteRequest
        ) -> NoteSchema:
        async with self.async_session.begin() as session:
            note = await session.execute(
                select(Note).where(
                    (Note.created_by == user_id) &
                    (Note.note_id == note_id) &
                    (Note.deleted_at == None)
                )
            )
            note = note.scalars().first()
            if not note:
                raise HTTPException(status_code=404)

            note.title = request.new_title
            note.content = request.new_content
            note.updated_at = datetime.datetime.utcnow()
            note.updated_by = user_id

            await session.flush()

            return NoteSchema.from_orm(note)

class DeleteNote:
    def __init__(self, session: AsyncSession) -> None:
        self.async_session = session

    async def execute(
        self,
        user_id: int,
        note_id: int
    ) -> NoteSchema:
        async with self.async_session.begin() as session:
            note = await session.execute(
                select(Note).where(
                    (Note.created_by == user_id) &
                    (Note.note_id == note_id) &
                    (Note.deleted_at == None)
                )
            )
            note = note.scalars().first()
            if not note:
                raise HTTPException(status_code=404)

            note.deleted_at = datetime.datetime.utcnow()
            note.deleted_by = user_id

            await session.flush()

            return NoteSchema.from_orm(note)
