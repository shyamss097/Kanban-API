from pydantic import BaseModel, Field
from datetime import timedelta, datetime
from typing import List, Optional

class Task(BaseModel):
    name: str
    description: str
    status: str 

class BoardCreate(BaseModel):
    title: str
    description: str

class Board(BaseModel):
    id: str
    title: str
    description: str
    created_at: datetime

class ListCreate(BaseModel):
    title: str
    board_id: str

class List(BaseModel):
    id: str
    title: str
    board_id: str
    created_at: datetime

class TaskCreate(BaseModel):
    title: str
    description: str
    list_id: str

class Task(BaseModel):
    id: str
    title: str
    description: str
    list_id: str
    created_at: datetime
