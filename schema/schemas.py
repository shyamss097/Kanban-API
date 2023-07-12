def individual_serial(task) -> dict:
    return{
        "id": str(task["_id"]),
        "name": task["name"],
        "description": task["description"],
        "status": task["status"]
    }

def list_serial(tasks) -> list:
    return[individual_serial(task) for task in tasks]
        
    