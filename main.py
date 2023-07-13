from fastapi import FastAPI

app = FastAPI(
    docs_url="/docs",
    redoc_url="/",
    title = "Kanban API",
    description="An API designed to make easy the process of task management!",
    #openapi_url="/api/v2/openapi.json"
)

from routes.route import router
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

app.include_router(router)