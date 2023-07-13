from fastapi import APIRouter, Depends, HTTPException, Response
from fastapi.openapi.docs import get_swagger_ui_html
from models.task import *
from conf.database import * 
from schema.schemas import list_serial
from bson import ObjectId
from typing import List


import os




router = APIRouter()

# @router.get("/")
# def get_tasks():
#     tasks = list_serial(collection_name.find())
#     return tasks


# @router.post("/")
# def create_task(task:Task):
#     collection_name.insert_one(dict(task))
@router.get("/boards")
async def get_boards():
    boards = list(boards_collection.find())
    for board in boards:
        board["_id"] = str(board["_id"])
    return boards

@router.post("/boards")
async def create_board(board_name: str):
    board = {"name": board_name}
    result = boards_collection.insert_one(board)
    return {"id": str(result.inserted_id)}

@router.put("/boards/{board_id}")
async def update_board(board_id: str, board_name: str):
    query = {"_id": ObjectId(board_id)}
    update = {"$set": {"name": board_name}}
    boards_collection.update_one(query, update)
    return {"message": "Board updated successfully"}

@router.delete("/boards/{board_id}")
async def delete_board(board_id: str):
    query = {"_id": ObjectId(board_id)}
    boards_collection.delete_one(query)
    return {"message": "Board deleted successfully"}


# List CRUD operations
@router.post("/boards/{board_id}/lists")
async def create_list(board_id: str, list_name: str):
    query = {"_id": ObjectId(board_id)}
    board = boards_collection.find_one(query)
    if not board:
        return {"message": "Board not found"}
    new_list = {"name": list_name, "board_id": ObjectId(board_id)}
    result = lists_collection.insert_one(new_list)
    return {"id": str(result.inserted_id)}

@router.put("/lists/{list_id}")
async def update_list(list_id: str, list_name: str):
    query = {"_id": ObjectId(list_id)}
    update = {"$set": {"name": list_name}}
    lists_collection.update_one(query, update)
    return {"message": "List updated successfully"}

@router.delete("/lists/{list_id}")
async def delete_list(list_id: str):
    query = {"_id": ObjectId(list_id)}
    lists_collection.delete_one(query)
    return {"message": "List deleted successfully"}


# Task CRUD operations
@router.post("/lists/{list_id}/tasks")
async def create_task(list_id: str, task_name: str):
    query = {"_id": ObjectId(list_id)}
    list = lists_collection.find_one(query)
    if not list:
        return {"message": "List not found"}
    new_task = {"name": task_name, "list_id": ObjectId(list_id)}
    result = tasks_collection.insert_one(new_task)
    return {"id": str(result.inserted_id)}

@router.put("/tasks/{task_id}")
async def update_task(task_id: str, task_name: str):
    query = {"_id": ObjectId(task_id)}
    update = {"$set": {"name": task_name}}
    tasks_collection.update_one(query, update)
    return {"message": "Task updated successfully"}

@router.delete("/tasks/{task_id}")
async def delete_task(task_id: str):
    query = {"_id": ObjectId(task_id)}
    tasks_collection.delete_one(query)
    return {"message": "Task deleted successfully"}