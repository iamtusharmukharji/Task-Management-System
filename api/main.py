from fastapi import FastAPI, Depends
from fastapi.responses import JSONResponse
from .routers.endpoints import router
from starlette.responses import RedirectResponse
from api.db import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import text
from . import docs

app = FastAPI(
    title="Task Management System [FastAPI Assignment]",
    version="0.1.0",
    openapi_tags=docs.openapi_tags_metadata
    )


app.include_router(router)


@app.get("/", include_in_schema=False)
def main():
    return RedirectResponse(url="/docs/")


@app.get("/health_check", status_code=200, tags=["DB Health"])
async def db_health_check(db: AsyncSession = Depends(get_db)):
    """
    Check database connection.

    **Response:**
    - **status**: connection status
    - **message**: confirmation message

    **Errors:**
    - Returns `400` for any unexpected error or failed db connection
    """
    try:
        # run simple sql query to check db connection status
        await db.execute(text("SELECT 1"))
        return {"status": "ok", "message": "database is healthy"}
    
    except Exception as err:
        response = {"status": "error", "message": f"database connection failed: {str(err)}"}
        return JSONResponse(content=response, status_code=400)


# uvicorn app.main:app --reload

# alembic revision --autogenerate -m "Initial migration"
# alembic upgrade head
