from datetime import datetime
from typing import List
from fastapi import APIRouter, HTTPException, status
from app.models import Item, ItemCreate, ItemUpdate, ItemResponse
from app.database import get_db

router = APIRouter(prefix="/items", tags=["Items"])


def row_to_item(row) -> Item:
    return Item(
        id=row["id"],
        name=row["name"],
        description=row["description"],
        price=row["price"],
        is_active=bool(row["is_active"]),
        created_at=datetime.fromisoformat(row["created_at"]),
        updated_at=datetime.fromisoformat(row["updated_at"]),
    )


@router.get("", response_model=List[Item])
def list_items(skip: int = 0, limit: int = 100):
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM items ORDER BY id DESC LIMIT ? OFFSET ?",
            (limit, skip)
        )
        rows = cursor.fetchall()
        return [row_to_item(row) for row in rows]


@router.get("/{item_id}", response_model=ItemResponse)
def get_item(item_id: int):
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM items WHERE id = ?", (item_id,))
        row = cursor.fetchone()
        if not row:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Item with id {item_id} not found"
            )
        return ItemResponse(success=True, data=row_to_item(row))


@router.post("", response_model=ItemResponse, status_code=status.HTTP_201_CREATED)
def create_item(item: ItemCreate):
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO items (name, description, price, is_active)
            VALUES (?, ?, ?, ?)
            """,
            (item.name, item.description, item.price, int(item.is_active))
        )
        item_id = cursor.lastrowid
        cursor.execute("SELECT * FROM items WHERE id = ?", (item_id,))
        row = cursor.fetchone()
        return ItemResponse(
            success=True,
            data=row_to_item(row),
            message="Item created successfully"
        )


@router.put("/{item_id}", response_model=ItemResponse)
def update_item(item_id: int, item: ItemUpdate):
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM items WHERE id = ?", (item_id,))
        existing = cursor.fetchone()
        if not existing:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Item with id {item_id} not found"
            )
        
        update_data = item.model_dump(exclude_unset=True)
        if not update_data:
            return ItemResponse(success=True, data=row_to_item(existing))
        
        if "is_active" in update_data:
            update_data["is_active"] = int(update_data["is_active"])
        
        set_clause = ", ".join(f"{k} = ?" for k in update_data.keys())
        values = list(update_data.values()) + [item_id]
        
        cursor.execute(
            f"UPDATE items SET {set_clause} WHERE id = ?",
            values
        )
        cursor.execute("SELECT * FROM items WHERE id = ?", (item_id,))
        row = cursor.fetchone()
        return ItemResponse(
            success=True,
            data=row_to_item(row),
            message="Item updated successfully"
        )


@router.delete("/{item_id}", response_model=ItemResponse)
def delete_item(item_id: int):
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM items WHERE id = ?", (item_id,))
        existing = cursor.fetchone()
        if not existing:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Item with id {item_id} not found"
            )
        
        cursor.execute("DELETE FROM items WHERE id = ?", (item_id,))
        return ItemResponse(
            success=True,
            data=row_to_item(existing),
            message="Item deleted successfully"
        )
