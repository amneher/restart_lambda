from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class ItemBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=500)
    url: str = Field(..., min_length=10, max_length=250)
    retailer: Optional[str] = Field(None, max_length=100)
    affiliate_status: Optional[str] = Field(None, max_length=50)
    price: float = Field(..., gt=0)
    quantity_needed: int = Field(default=1, ge=1)
    quantity_purchased: int = Field(default=0, ge=0)
    is_active: bool = Field(default=True)


class ItemCreate(ItemBase):
    pass


class ItemUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=500)
    price: Optional[float] = Field(None, gt=0)
    quantity_needed: Optional[int] = Field(None, ge=1)
    quantity_purchased: Optional[int] = Field(None, ge=0)
    is_active: Optional[bool] = None


class Item(ItemBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime
    updated_at: datetime


class ItemResponse(BaseModel):
    success: bool
    data: Optional[Item] = None
    message: Optional[str] = None
