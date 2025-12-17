import json
from pathlib import Path
from typing import Dict

from fastapi import APIRouter, HTTPException

from models import Item

router = APIRouter()

# Path to the JSON database relative to the project root (or container WORKDIR)
DB_PATH: Path = Path("data/db.json")


def check_database_exists() -> None:
    """
    Ensure the JSON database file exists.

    In local dev:   ./data/db.json
    In Docker:      <path_data>/db.json mounted to /app/data/db.json
    """
    if not DB_PATH.exists():
        print(f"ERROR: Database file not found at {DB_PATH}")
        print("In local development: create data/db.json manually.")
        print("In Docker: mount a volume or bind mount so that data/db.json exists.")
        raise FileNotFoundError(f"Database file not found: {DB_PATH}")


def load_database() -> Dict:
    """Load data from JSON file and return as dictionary."""
    with open(DB_PATH, "r") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError as exc:
            raise ValueError("Database file is not valid JSON.") from exc


def save_database(data: Dict) -> None:
    """Persist dictionary data back to the JSON file."""
    with open(DB_PATH, "w") as f:
        json.dump(data, f, indent=2)


@router.get("/")
async def root():
    return {
        "message": "Welcome to the Items API!",
        "database": str(DB_PATH),
    }


@router.get("/health")
async def health_check():
    db = load_database()
    items = db.get("items", {})
    return {
        "status": "healthy",
        "items_count": len(items),
    }


@router.get("/items")
async def list_items():
    db = load_database()
    items = db.get("items", {})
    return {"items": items}


@router.get("/items/{item_id}")
async def read_item(item_id: str):
    db = load_database()
    items = db.get("items", {})

    if item_id not in items:
        raise HTTPException(status_code=404, detail="Item not found")

    return items[item_id]


@router.post("/items/")
async def create_item(item: Item):
    db = load_database()

    items = db.get("items")
    if items is None:
        items = {}
        db["items"] = items

    new_id = str(len(items) + 1)
    items[new_id] = item.model_dump()

    save_database(db)

    return {
        "message": "Item created successfully",
        "item_id": new_id,
        "item": items[new_id],
    }


@router.put("/items/{item_id}")
async def update_item(item_id: str, item: Item):
    db = load_database()
    items = db.get("items", {})

    if item_id not in items:
        raise HTTPException(status_code=404, detail="Item not found")

    items[item_id] = item.model_dump()
    save_database(db)

    return {
        "message": "Item updated successfully",
        "item_id": item_id,
        "item": items[item_id],
    }


@router.delete("/items/{item_id}")
async def delete_item(item_id: str):
    db = load_database()
    items = db.get("items", {})

    if item_id not in items:
        raise HTTPException(status_code=404, detail="Item not found")

    deleted_item = items.pop(item_id)
    save_database(db)

    return {
        "message": "Item deleted successfully",
        "item": deleted_item,
    }