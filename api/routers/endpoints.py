from fastapi import APIRouter, Depends, Query, Path
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from ..db import get_db
from ..schemas import NewTask, UpdateTask
from api import models
from datetime import datetime
import uuid

router = APIRouter(prefix="/task", tags=['Tasks'])


# Endpoint to get all the task with paginated query
@router.get("/all", status_code=200)
async def get_all_tasks(
                        db: AsyncSession = Depends(get_db),
                        page: int = Query(1, ge=1),
                        size: int = Query(10, ge=1, le=100),
                        ):
    """
    Fetch paginated list of tasks.

    **Request Parameters:**
    - **page**: Page number (default: 1)
    - **size**: Number of tasks per page (default: 10, max: 100)

    **Errors:**
    - Returns `400` for any unexpected error
    """

    try:

        # count of total tasks in db
        total_count_query = await db.execute(select(models.Tasks))
        total_tasks = len(total_count_query.scalars().all())

        offset = (page - 1) * size  

        # ORM query for fethcing paginated tasks
        db_tasks_query = select(models.Tasks).limit(size).offset(offset)
        db_tasks = await db.execute(db_tasks_query)
        db_tasks = db_tasks.scalars().unique().all()

        return {

            "total_tasks": total_tasks,
            "total_pages": (total_tasks + size - 1) // size,
            "current_page": page,
            "tasks_per_page": size,
            "tasks": db_tasks
        }

        
        
    except Exception as err:
        
        return JSONResponse(content={"message":str(err)}, status_code=400)

 
# Endpoint for creating new task with pydantic validation of payload
@router.post("/new", status_code=201)
async def create_task(
                        newTaskPayload: NewTask,
                        db: AsyncSession = Depends(get_db)
                        ):
    """
    Create a new task.

    **Request Body:**
    - **title**: (str) Title of the task (Required)
    - **description**: (str) Detailed description of the task (Required)
    - **status**: (str) Status of the task (e.g., "pending", "completed", "in-progress") (Required)

    **Response:**
    - **message**: Confirmation message
    - **task_id**: ID of the newly created task

    **Errors:**
    - Returns `400` for any unexpected error
    """

    try:

        #initialize and adding a new Task
        new_task = models.Tasks(
            title = newTaskPayload.title,
            description = newTaskPayload.description,
            status = newTaskPayload.status
        )

        db.add(new_task)
        
        await db.commit()
        await db.refresh(new_task)
        
        return {"message":"task has been created", "task_id":str(new_task.id)}
        
    except Exception as err:
        
        return JSONResponse(content={"message":str(err)}, status_code=400)


# Endpoint for updating an existing task with taskId
@router.patch("/update/{taskId}", status_code=200)
async def update_task(
                        
                        updateTaskPayload: UpdateTask,
                        taskId: uuid.UUID = Path(..., description="Item ID must be a valid UUID"),
                        db: AsyncSession = Depends(get_db)
                        ):
    """
    Update an existing task.

    **Path Parameter:**
    - **taskId**: (UUID) Unique identifier of the task to update (Required)

    **Request Body:**
    - **title**: (str) Updated title of the task (Optional)
    - **status**: (str) Updated status of the task (e.g., "pending", "completed") (Optional)

    **Response:**
    - **message**: Confirmation message
    - **task_id**: ID of the updated task

     **Errors:**
    - Returns `404` if the task is not found
    - Returns `400` for any unexpected error or invalid payload
    """
    try:

        # get task to be updated
        db_task = await db.get(models.Tasks,taskId)

        # validate the existance of requested task
        if not db_task:
            return JSONResponse(content={"message":"task not found"}, status_code=404)
        
        # validate the completely empty json payload
        if updateTaskPayload.title == None and updateTaskPayload.status == None:
            return JSONResponse(content={"message":"invalid payload"}, status_code=400)
        
        # if user requested to update title
        if updateTaskPayload.title:
            db_task.title = updateTaskPayload.title

        # if user requested to update status
        if updateTaskPayload.status:
            db_task.status = updateTaskPayload.status

        db_task.updated_at = datetime.now()

        await db.commit()
        
        return {"message":"task has been updated", "task_id":str(db_task.id)}

        
    except Exception as err:
        
        return JSONResponse(content={"message":str(err)}, status_code=400)
    

# Endpoint for deleting an existing task with taskId
@router.delete("/delete/{taskId}", status_code=200)
async def delete_task(
                        taskId: uuid.UUID = Path(..., description="Item ID must be a valid UUID"),
                        db: AsyncSession = Depends(get_db)
                        ):
    """
    Delete a task by its ID.

    **Path Parameter:**
    - **taskId**: (UUID) Unique identifier of the task to delete (Required)

    **Response:**
    - **message**: Confirmation message if the task is deleted with status code 200

    **Errors:**
    - Returns `404` if the task is not found
    - Returns `400` for any unexpected error
    """
    try:

        # get task requested by user
        db_task = await db.get(models.Tasks,taskId)

        # null check of requested task
        if not db_task:
            return JSONResponse(content={"message":"task not found"}, status_code=404)
        
        
        await db.delete(db_task)
        await db.commit()

        return {"message":"task has been deleted"}

        
    except Exception as err:
        
        return JSONResponse(content={"message":str(err)}, status_code=400)
