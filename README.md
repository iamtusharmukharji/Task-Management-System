# Task-Management-System
Task Management System built on FastAPI with Alembic for db migrations

## Steps to run project on localhost

Note:- database credentials like user, password and databaseName is defined in api/credentials/credentials.json you can change as per config of your system

> 1. Install dependecies from requirements.txt file
                    
  `pip install -r requirements.txt`

> 2. Create initial migrations
                    
  `alembic revision --autogenerate -m "Initial migration"`

> 3. Apply initial migrations
                    
  `alembic upgrade head`

> 4. Run main.py from app
                    
  `uvicorn app.main:app --reload`

> 5. Run unit test cases
                    
  `pytest --asyncio-mode=auto`



### navigate to  [localhost:8000](http://localhost:8000) once application is running