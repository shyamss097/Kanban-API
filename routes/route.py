from fastapi import APIRouter, Depends, HTTPException
from fastapi.openapi.docs import get_swagger_ui_html
from models.task import *
from conf.database import * 
from schema.schemas import list_serial
from bson import ObjectId


import os




router = APIRouter()

# @router.get("/")
# def get_tasks():
#     tasks = list_serial(collection_name.find())
#     return tasks


# @router.post("/")
# def create_task(task:Task):
#     collection_name.insert_one(dict(task))

@router.post("/boards", response_model=Board)
async def create_board(board: BoardCreate):
    board_dict = board.dict()
    board_dict["created_at"] = datetime.utcnow()
    board_id = str(boards_collection.insert_one(board_dict).inserted_id)
    board_dict["id"] = board_id
    return board_dict

@router.get("/boards", response_model=list[Board])
async def get_boards():
    return list(boards_collection.find())

@router.get("/boards/{board_id}", response_model=Board)
async def get_board(board_id: str):
    board = boards_collection.find_one({"_id": ObjectId(board_id)})
    if not board:
        raise HTTPException(status_code=404, detail="Board not found")
    return board

@router.put("/boards/{board_id}", response_model=Board)
async def update_board(board_id: str, board: BoardCreate):
    existing_board = boards_collection.find_one({"_id": ObjectId(board_id)})
    if not existing_board:
        raise HTTPException(status_code=404, detail="Board not found")
    updated_board = board.dict(exclude_unset=True)
    boards_collection.update_one({"_id": ObjectId(board_id)}, {"$set": updated_board})
    return {**existing_board, **updated_board}

@router.delete("/boards/{board_id}")
async def delete_board(board_id: str):
    result = boards_collection.delete_one({"_id": ObjectId(board_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Board not found")
    # Delete associated lists and tasks
    lists_collection.delete_many({"board_id": board_id})
    tasks_collection.delete_many({"list_id": {"$in": list(lists_collection.find({"board_id": board_id}, {"_id": 1}))}})
    return {"message": "Board deleted"}

@router.post("/lists", response_model=List)
async def create_list(list: ListCreate):
    list_dict = list.dict()
    board_id = list_dict["board_id"]
    board = boards_collection.find_one({"_id": ObjectId(board_id)})
    if not board:
        raise HTTPException(status_code=404, detail="Board not found")
    list_dict["created_at"] = datetime.utcnow()
    list_id = str(lists_collection.insert_one(list_dict).inserted_id)
    list_dict["id"] = list_id
    return list_dict

@router.get("/lists/{list_id}", response_model=List)
async def get_list(list_id: str):
    list_item = lists_collection.find_one({"_id": ObjectId(list_id)})
    if not list_item:
        raise HTTPException(status_code=404, detail="List not found")
    return list_item

@router.put("/lists/{list_id}", response_model=List)
async def update_list(list_id: str, list: ListCreate):
    existing_list = lists_collection.find_one({"_id": ObjectId(list_id)})
    if not existing_list:
        raise HTTPException(status_code=404, detail="List not found")
    updated_list = list.dict(exclude_unset=True)
    lists_collection.update_one({"_id": ObjectId(list_id)}, {"$set": updated_list})
    return {**existing_list, **updated_list}

@router.delete("/lists/{list_id}")
async def delete_list(list_id: str):
    result = lists_collection.delete_one({"_id": ObjectId(list_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="List not found")
    # Delete associated tasks
    tasks_collection.delete_many({"list_id": list_id})
    return {"message": "List deleted"}

@router.get("/docs", include_in_schema=False)
async def custom_swagger_ui_html_cdn():
    return get_swagger_ui_html(
    openapi_url=router.openapi_url,
    title=f"{router.title} - Swagger UI",
    # swagger_ui_dark.css CDN link
    swagger_css_url="https://cdn.jsdelivr.net/gh/Itz-fork/Fastapi-Swagger-UI-Dark/assets/swagger_ui_dark.min.css"
)