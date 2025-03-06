from pydantic import BaseModel
import enum
from uuid import UUID
from datetime import datetime
from typing import Optional

# Pydantic models

# Enum class for status
class TaskStatus(str,enum.Enum):
    PENDING = "pending"
    IN_PROGRESS = "in-progress"
    COMPLETED = "completed"

# payload for new task
class NewTask(BaseModel):
    title: str
    description: str
    status: TaskStatus

# payload for Updating an existing task
class UpdateTask(BaseModel):
    title: Optional[str] = None
    status: Optional[TaskStatus] = None

# Pydantic class for serializing Tasks objects
class TaskResponse(BaseModel):
    id: UUID
    title: str
    description: str
    status: str
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True