from fastapi import APIRouter, Depends, Path, Request, Response, HTTPException
from api.base.base_schemas import BaseResponse, PaginationParams
from middlewares.authentication import get_user_id_from_access_token

from .schemas import (
    CreateNoteRequest,
    CreateNoteResponse,
    NotePaginationResponse,
    ReadAllNoteResponse,
    ReadNoteResponse,
    UpdateNoteRequest,
    UpdateNoteResponse,
    DeleteNoteResponse
)
from .use_cases import CreateNote, ReadAllNote, ReadNote, UpdateNote, DeleteNote

router = APIRouter(prefix="/notes")
tag = "Note"

@router.post("", response_model=CreateNoteResponse, tags=[tag])
async def create_note(
    request: Request,
    response: Response,
    data: CreateNoteRequest,
    token_user_id: int = Depends(get_user_id_from_access_token),
    create_note: CreateNote = Depends(CreateNote),
) -> CreateNoteResponse:
    """
    This API endpoint is for create a new note.
    """
    try:
        resp_data = await create_note.execute(
            user_id=token_user_id,
            request=data,
        )

        return CreateNoteResponse(
            status="success",
            message="success create new note",
            data=resp_data,
        )

    except HTTPException as ex:
        response.status_code = ex.status_code
        return CreateNoteResponse(
            status="error",
            message=ex.detail,
        )

    except Exception as e:
        response.status_code = 500
        message = "failed to create new note"
        if hasattr(e, "message"):
            message = e.message
        elif hasattr(e, "detail"):
            message = e.detail

        return CreateNoteResponse(
            status="error",
            message=message,
        )

@router.get("", response_model=ReadAllNoteResponse, tags=[tag])
async def read_all(
    request: Request,
    response: Response,
    token_user_id: int = Depends(get_user_id_from_access_token),
    filter_user: bool = True,
    include_deleted: bool = False,
    page_params: PaginationParams = Depends(),
    read_all: ReadAllNote = Depends(ReadAllNote),
) -> ReadAllNoteResponse:
    """
    This API endpoint is for read all notes.
    """
    try:
        resp_data = await read_all.execute(
            user_id=token_user_id,
            page_params=page_params,
            filter_user=filter_user,
            include_deleted=include_deleted
        )

        return ReadAllNoteResponse(
            status="success",
            message="success read all notes",
            data=NotePaginationResponse(records=resp_data[0], meta=resp_data[1]),
        )

    except HTTPException as ex:
        response.status_code = ex.status_code
        return ReadAllNoteResponse(
            status="error",
            message=ex.detail,
        )

    except Exception as e:
        response.status_code = 500
        message = "failed to read all notes"
        if hasattr(e, "message"):
            message = e.message
        elif hasattr(e, "detail"):
            message = e.detail

        return ReadAllNoteResponse(
            status="error",
            message=message,
        )

@router.get("/{note_id}", response_model=ReadNoteResponse, tags=[tag])
async def read_one_note(
    request: Request,
    response: Response,
    note_id: int = Path(..., description=""),
    token_user_id: int = Depends(get_user_id_from_access_token),
    read_note: ReadNote = Depends(ReadNote),
) -> ReadNoteResponse:
    """
    This API endpoint is for read one note.
    """
    try:
        resp_data = await read_note.execute(
            user_id=token_user_id,
            note_id=note_id
        )

        return ReadNoteResponse(
            status="success",
            message=f"success read note with id={note_id}",
            data=resp_data,
        )

    except HTTPException as ex:
        response.status_code = ex.status_code
        return ReadNoteResponse(
            status="error",
            message=ex.detail,
        )

    except Exception as e:
        response.status_code = 500
        message = f"failed to read note with id={note_id}"
        if hasattr(e, "message"):
            message = e.message
        elif hasattr(e, "detail"):
            message = e.detail

        return ReadNoteResponse(
            status="error",
            message=message,
        )

@router.put("/{note_id}", response_model=UpdateNoteResponse, tags=[tag])
async def update_note(
    request: Request,
    response: Response,
    data: UpdateNoteRequest,
    note_id: int = Path(..., description=""),
    token_user_id: int = Depends(get_user_id_from_access_token),
    update_note: UpdateNote = Depends(UpdateNote),
) -> UpdateNoteResponse:
    """
    This API endpoint is for update existing note.
    """
    try:
        resp_data = await update_note.execute(
            user_id=token_user_id,
            note_id=note_id,
            request=data)

        return UpdateNoteResponse(
            status="success",
            message=f"success update note with id={note_id}",
            data=resp_data,
        )

    except HTTPException as ex:
        response.status_code = ex.status_code
        return UpdateNoteResponse(
            status="error",
            message=ex.detail,
        )

    except Exception as e:
        response.status_code = 500
        message = f"failed to update note with id={note_id}"
        if hasattr(e, "message"):
            message = e.message
        elif hasattr(e, "detail"):
            message = e.detail

        return UpdateNoteResponse(
            status="error",
            message=message,
        )

@router.delete("/{note_id}", response_model=DeleteNoteResponse, tags=[tag])
async def delete_note(
    response: Response,
    request: Request,
    note_id: int = Path(..., description=""),
    token_user_id: int = Depends(get_user_id_from_access_token),
    delete_note: DeleteNote = Depends(DeleteNote),
) -> DeleteNoteResponse:
    """
    This API endpoint is for delete existing note.
    """
    try:
        resp_data = await delete_note.execute(
            user_id=token_user_id,
            note_id=note_id
        )

        return DeleteNoteResponse(
            status="success",
            message=f"success delete user with id={note_id}",
            data=resp_data,
        )

    except HTTPException as ex:
        response.status_code = ex.status_code
        return DeleteNoteResponse(
            status="error",
            message=ex.detail,
        )

    except Exception as e:
        response.status_code = 500
        message = f"error delete user with id={note_id}"
        if hasattr(e, "message"):
            message = e.message
        elif hasattr(e, "detail"):
            message = e.detail

        return DeleteNoteResponse(
            status="error",
            message=message,
        )
