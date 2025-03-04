from fastapi import APIRouter, Depends, Query
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.db import get_db
from app.schemas import NewTask, UpdateTask
import app.models as models 
from datetime import datetime

router = APIRouter(prefix="/task")



@router.get("/all", status_code=200)
async def get_all_tasks(
                        db: AsyncSession = Depends(get_db),
                        page: int = Query(1, ge=1),
                        taskPerPage: int = Query(10, ge=1, le=100),
                        ):
    try:

    
        total_count_query = await db.execute(select(models.Tasks))
        total_tasks = len(total_count_query.scalars().all())

        offset = (page - 1) * taskPerPage  

        db_tasks_query = select(models.Tasks).limit(taskPerPage).offset(offset)
        db_tasks = await db.execute(db_tasks_query)
        db_tasks = db_tasks.scalars().unique().all()

        return {
            "total_tasks": total_tasks,
            "total_pages": (total_tasks + taskPerPage - 1) // taskPerPage,
            "current_page": page,
            "tasks_per_page": taskPerPage,
            "tasks": db_tasks
        }

        
        
    except Exception as err:
        
        return JSONResponse(content={"message":str(err)}, status_code=400)

 

@router.post("/new", status_code=201)
async def create_task(
                        newTaskPayload: NewTask,
                        db: AsyncSession = Depends(get_db)
                        ):
    try:

        new_task = models.Tasks(
            title = newTaskPayload.title,
            description = newTaskPayload.description,
            status = newTaskPayload.status
        )

        db.add(new_task)
        
        await db.commit()
        await db.refresh(new_task)
        
        return {"message":"task has been created", "task_id":str(new_task.id)}

        #return JSONResponse(content=resp, status_code=201)
        
    except Exception as err:
        
        return JSONResponse(content={"message":str(err)}, status_code=400)

    
@router.put("/update", status_code=200)
async def update_task(
                        taskId: str,
                        updateTaskPayload: UpdateTask,
                        db: AsyncSession = Depends(get_db)
                        ):
    try:

        db_task = await db.get(models.Tasks,taskId)

        if not db_task:
            return JSONResponse(content={"message":"task not found"}, status_code=404)
        
        if updateTaskPayload.title == None and updateTaskPayload.status == None:
            return JSONResponse(content={"message":"invalid payload"}, status_code=400)
        
        
        if updateTaskPayload.title:
            db_task.title = updateTaskPayload.title
        if updateTaskPayload.status:
            db_task.status = updateTaskPayload.status

        db_task.updated_at = datetime.now()

        await db.commit()
        
        return {"message":"task has been updated"}

        
    except Exception as err:
        
        return JSONResponse(content={"message":str(err)}, status_code=400)

@router.delete("/delete/{taskId}", status_code=200)
async def delete_task(
                        taskId: str,
                        db: AsyncSession = Depends(get_db)
                        ):
    try:

        db_task = await db.get(models.Tasks,taskId)

        if not db_task:
            return JSONResponse(content={"message":"task not found"}, status_code=404)
        
        
        await db.delete(db_task)
        await db.commit()

        return {"message":"task has been deleted"}

        
    except Exception as err:
        
        return JSONResponse(content={"message":str(err)}, status_code=400)
