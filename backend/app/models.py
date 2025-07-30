import uuid
from datetime import datetime

from pydantic import BaseModel, Field


class DocumentUpload(BaseModel):
    filename: str
    content: bytes


class DocumentSummary(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    filename: str
    summary: str
    upload_date: datetime = Field(default_factory=datetime.now)


class DocumentHistory(BaseModel):
    id: str
    filename: str
    summary: str
    upload_date: datetime
