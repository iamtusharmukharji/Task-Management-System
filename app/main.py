from fastapi import FastAPI, Depends
from app.endpoints import router
from starlette.responses import RedirectResponse
from app.db import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import text

app = FastAPI(
    title="Task Management System [FastAPI Assignment]",
    version="0.1.0",
    )


app.include_router(router)

@app.get("/", include_in_schema=False)
def main():
    return RedirectResponse(url="/docs/")


@app.get("/health_check", status_code=200)
async def db_health_check(db: AsyncSession = Depends(get_db)):
    try:
        await db.execute(text("SELECT 1"))
        return {"status": "ok", "message": "database is healthy"}
    
    except Exception as err:
        return {"status": "error", "message": f"database connection failed: {str(err)}"}
    
# uvicorn app.main:app --reload

# alembic revision --autogenerate -m "Initial migration"
# alembic upgrade head
