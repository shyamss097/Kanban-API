from pymongo import MongoClient

client = MongoClient("mongodb+srv://admin:pass1234@mycluster.umbxht1.mongodb.net/?retryWrites=true&w=majority")

db = client.kanban_db

collection_name = db['task_collection']
boards_collection = db["boards"]
lists_collection = db["lists"]
tasks_collection = db["tasks"]
users_collection = db["users"]