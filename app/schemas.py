from pydantic import BaseModel
import enum
from uuid import UUID
from datetime import datetime
from typing import Optional

class TaskStatus(str,enum.Enum):
    PENDING = "pending"
    IN_PROGRESS = "in-progress"
    COMPLETED = "completed"

class NewTask(BaseModel):
    title: str
    description: str
    status: TaskStatus

class UpdateTask(BaseModel):
    title: Optional[str] = None
    status: Optional[TaskStatus] = None

class TaskResponse(BaseModel):
    id: UUID
    title: str
    description: str
    status: str
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True