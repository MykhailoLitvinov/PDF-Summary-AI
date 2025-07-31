import uuid
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class DocumentUpload(BaseModel):
    filename: str
    content: bytes


class DocumentSummary(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    filename: str
    summary: str
    upload_date: datetime = Field(default_factory=datetime.now)
    file_size: int
    page_count: int


class DocumentHistory(BaseModel):
    id: str
    filename: str
    summary: str
    upload_date: datetime
    file_size: int
    page_count: int

class APIResponse(BaseModel):
    success: bool
    message: str
    data: Optional[dict] = None
