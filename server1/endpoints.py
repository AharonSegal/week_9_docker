print("222222222222222222222222222222222222")
import json
from pathlib import Path
from typing import List, Dict
from fastapi import APIRouter
from models import Item

router = APIRouter()

# Path to the JSON database 
# DB_PATH: Path = Path("C:\Users\a0527\שולחן העבודה\TEST_DOCKER\week_9_docker\server1\db\shopping_list.json")
DB_PATH: Path = Path("db/shopping_list.json")

print("3333333333333333333333333333333333333333")

#   +---------------------+
#   |        UTILS        |   
#   +---------------------+ 

def check_database_exists() -> None:
    """
    Ensure the JSON database file exists.

    In local dev:   ./db\shopping_list.json
    In Docker:      <path_data>/db.json mounted to /app/db\shopping_list.json
    """
    if not DB_PATH.exists():
        print("4444444444444  PATH  :", DB_PATH)
        print(f"ERROR: Database file not found at {DB_PATH}")
        print("In local development: create db\shopping_list.json manually.")
        print("In Docker: mount a volume or bind mount so that db\shopping_list.json exists.")
        raise FileNotFoundError(f"Database file not found: {DB_PATH}")


def load_database() -> List[Dict]:
    try:
        with open(DB_PATH, "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return [] # Return empty list if file doesn't exist or is empty

def save_database(data: List[Dict]) -> None:
    with open(DB_PATH, "w") as f:
        json.dump(data, f, indent=2)

#   +---------------------+
#   |       PART ONE      |   
#   +---------------------+ 

@router.get("/items")
async def list_items():
    # load and print the item list
    db = load_database()
    return db

@router.post("/items/")
async def create_item(name: str, quantity: int):
    db = load_database()
    # for first entry
    if not db:
        db = []

    # auto increment
    new_id = len(db) + 1
    
    # create new item
    new_item = Item(id=new_id, name=name, quantity=quantity)
    
    # converts obj dict
    db.append(new_item.model_dump())

    save_database(db)

    return {
        "message": "Item created successfully",
        "item": new_item
    }

