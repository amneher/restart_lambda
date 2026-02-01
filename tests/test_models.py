import pytest
from datetime import datetime
from pydantic import ValidationError
from app.models import Item, ItemCreate, ItemUpdate, ItemResponse


class TestItemCreate:
    def test_valid_item_create(self):
        item = ItemCreate(name="Test", description="A test", price=10.00)
        assert item.name == "Test"
        assert item.description == "A test"
        assert item.price == 10.00
        assert item.is_active is True

    def test_item_create_without_description(self):
        item = ItemCreate(name="Test", price=10.00)
        assert item.description is None

    def test_item_create_invalid_price(self):
        with pytest.raises(ValidationError):
            ItemCreate(name="Test", price=0)

    def test_item_create_negative_price(self):
        with pytest.raises(ValidationError):
            ItemCreate(name="Test", price=-5.00)

    def test_item_create_empty_name(self):
        with pytest.raises(ValidationError):
            ItemCreate(name="", price=10.00)

    def test_item_create_name_too_long(self):
        with pytest.raises(ValidationError):
            ItemCreate(name="x" * 101, price=10.00)


class TestItemUpdate:
    def test_valid_partial_update(self):
        item = ItemUpdate(name="New Name")
        assert item.name == "New Name"
        assert item.description is None
        assert item.price is None

    def test_empty_update(self):
        item = ItemUpdate()
        assert item.model_dump(exclude_unset=True) == {}

    def test_update_with_all_fields(self):
        item = ItemUpdate(
            name="Updated",
            description="New desc",
            price=50.00,
            is_active=False
        )
        assert item.name == "Updated"
        assert item.description == "New desc"
        assert item.price == 50.00
        assert item.is_active is False


class TestItem:
    def test_valid_item(self):
        now = datetime.now()
        item = Item(
            id=1,
            name="Test",
            description="Desc",
            price=10.00,
            is_active=True,
            created_at=now,
            updated_at=now
        )
        assert item.id == 1
        assert item.name == "Test"


class TestItemResponse:
    def test_success_response(self):
        now = datetime.now()
        item = Item(
            id=1,
            name="Test",
            description=None,
            price=10.00,
            is_active=True,
            created_at=now,
            updated_at=now
        )
        response = ItemResponse(success=True, data=item)
        assert response.success is True
        assert response.data.id == 1

    def test_error_response(self):
        response = ItemResponse(success=False, message="Not found")
        assert response.success is False
        assert response.data is None
        assert response.message == "Not found"
