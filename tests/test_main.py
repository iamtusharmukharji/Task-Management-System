

import pytest
import os
import sys
from httpx import AsyncClient


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))



@pytest.fixture
async def async_client():
    """Fixture to create an async test client"""
    async with AsyncClient(base_url="http://localhost:8000") as client:
        yield client


@pytest.mark.asyncio
async def test_create_task(async_client):

    response = await async_client.post("/task/new", json={
        "title": "Test Task",
        "description": "This is a test task",
        "status": "pending"
    })
    assert response.status_code == 201
    assert response.json()["message"] == "task has been created"


@pytest.mark.asyncio
async def test_create_task_invalid_status(async_client):

    response = await async_client.post("/task/new", json={
        "title": "Invalid Task",
        "description": "This task has an invalid status",
        "status": "unknown_status"
    })
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_get_tasks(async_client):

    response = await async_client.get("/task/all?page=1&size=10")
    assert response.status_code == 200

    data = response.json()

    assert "tasks" in data
    assert isinstance(data["tasks"], list)


@pytest.mark.asyncio
async def test_update_task(async_client):

    """Test updating a task"""
    # Create a new task first
    create_response = await async_client.post("/task/new", json={
        "title": "Task to update",
        "description": "This task will be updated",
        "status": "pending"
    })
    assert create_response.status_code == 201  # Ensure task was created

    task_id = create_response.json().get("task_id")
    assert task_id is not None

    # Update the task
    response = await async_client.patch(f"/task/update/{task_id}", json={
        "title": "Updated Task",
        "description": "Updated description"
    })
    assert response.status_code == 200
    assert response.json()["message"] == "task has been updated"


@pytest.mark.asyncio
async def test_delete_task(async_client):
    
    """Test deleting a task"""

    create_response = await async_client.post("/task/new", json={
        "title": "Task to delete",
        "description": "This task will be deleted",
        "status": "pending"
    })
    assert create_response.status_code == 201

    task_id = create_response.json().get("task_id")
    assert task_id is not None

    # Delete the created task
    delete_response = await async_client.delete(f"/task/delete/{task_id}")
    assert delete_response.status_code == 200 
    assert delete_response.json()["message"] == "task has been deleted"

    # Deleting again should return 404
    delete_again_response = await async_client.delete(f"/task/delete/{task_id}")
    assert delete_again_response.status_code == 404
