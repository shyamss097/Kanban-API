# Kanban API

This is a simple Kanban API built using FastAPI and MongoDB Atlas. It provides basic CRUD operations for managing boards, lists, and tasks.

## Prerequisites

- Python 3.7 or above
- FastAPI
- pymongo
- Uvicorn

## API Endpoints

- GET /boards - Retrieve all boards

- POST /boards - Create a new board

- PUT /boards/{board_id} - Update a board

- DELETE /boards/{board_id} - Delete a board

- POST /boards/{board_id}/lists - Create a new list for a specific board

- PUT /lists/{list_id} - Update a list

- DELETE /lists/{list_id} - Delete a list

- POST /lists/{list_id}/tasks - Create a new task for a specific list

- PUT /tasks/{task_id} - Update a task

- DELETE /tasks/{task_id} - Delete a task
