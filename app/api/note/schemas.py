from pydantic import BaseModel, Field
from api.base.base_schemas import BaseResponse, PaginationMetaResponse
from models.note import NoteSchema

# POST /notes
class CreateNoteRequest(BaseModel):
    title: str = Field(min_length=1, max_length=100)
    content: str = Field(min_length=6, max_length=500)

class CreateNoteResponse(BaseResponse):
    data: NoteSchema | None

# GET Pagination /notes
class NotePaginationResponse(BaseModel):
    records: list[NoteSchema]
    meta: PaginationMetaResponse
    # include_deleted: bool = False

class ReadAllNoteResponse(BaseResponse):
    data: NotePaginationResponse

# GET One Notes /notes/{id}
class ReadNoteResponse(BaseResponse):
    data: NoteSchema | None

# PUT /notes/{id}
class UpdateNoteRequest(BaseModel):
    new_title: str = Field(min_length=1, max_length=100)
    new_content: str = Field(min_length=6, max_length=500)

class UpdateNoteResponse(BaseResponse):
    data: NoteSchema | None

# DELETE /notes/{id}
class DeleteNoteResponse(BaseResponse):
    data: NoteSchema | None
