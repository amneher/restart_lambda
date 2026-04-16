

class TestCreateItem:
    def test_create_item_success(self, client, sample_item):
        response = client.post("/items", json=sample_item)
        assert response.status_code == 201
        data = response.json()
        assert data["success"] is True
        assert data["data"]["name"] == sample_item["name"]
        assert data["data"]["description"] == sample_item["description"]
        assert data["data"]["price"] == sample_item["price"]
        assert data["data"]["is_active"] == sample_item["is_active"]
        assert "id" in data["data"]
        assert "created_at" in data["data"]
        assert "updated_at" in data["data"]

    def test_create_item_without_description(self, client):
        item = {"name": "No Description", "url": "https://example.com/product/no-desc", "price": 15.00}
        response = client.post("/items", json=item)
        assert response.status_code == 201
        data = response.json()
        assert data["success"] is True
        assert data["data"]["description"] is None

    def test_create_item_invalid_price(self, client):
        item = {"name": "Invalid", "price": -10.00}
        response = client.post("/items", json=item)
        assert response.status_code == 422

    def test_create_item_missing_name(self, client):
        item = {"price": 10.00}
        response = client.post("/items", json=item)
        assert response.status_code == 422

    def test_create_item_empty_name(self, client):
        item = {"name": "", "price": 10.00}
        response = client.post("/items", json=item)
        assert response.status_code == 422


class TestGetItem:
    def test_get_item_success(self, client, sample_item):
        create_response = client.post("/items", json=sample_item)
        item_id = create_response.json()["data"]["id"]
        
        response = client.get(f"/items/{item_id}")
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert data["data"]["id"] == item_id
        assert data["data"]["name"] == sample_item["name"]

    def test_get_item_not_found(self, client):
        response = client.get("/items/99999")
        assert response.status_code == 404
        assert "not found" in response.json()["detail"].lower()


class TestListItems:
    def test_list_items_empty(self, client):
        response = client.get("/items")
        assert response.status_code == 200
        assert response.json() == []

    def test_list_items_with_data(self, client, sample_items):
        for item in sample_items:
            client.post("/items", json=item)
        
        response = client.get("/items")
        assert response.status_code == 200
        items = response.json()
        assert len(items) == 3

    def test_list_items_pagination(self, client, sample_items):
        for item in sample_items:
            client.post("/items", json=item)
        
        response = client.get("/items?skip=1&limit=1")
        assert response.status_code == 200
        items = response.json()
        assert len(items) == 1


class TestUpdateItem:
    def test_update_item_success(self, client, sample_item):
        create_response = client.post("/items", json=sample_item)
        item_id = create_response.json()["data"]["id"]
        
        update_data = {"name": "Updated Name", "price": 99.99}
        response = client.put(f"/items/{item_id}", json=update_data)
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert data["data"]["name"] == "Updated Name"
        assert data["data"]["price"] == 99.99
        assert data["data"]["description"] == sample_item["description"]

    def test_update_item_partial(self, client, sample_item):
        create_response = client.post("/items", json=sample_item)
        item_id = create_response.json()["data"]["id"]
        
        update_data = {"is_active": False}
        response = client.put(f"/items/{item_id}", json=update_data)
        assert response.status_code == 200
        data = response.json()
        assert data["data"]["is_active"] is False
        assert data["data"]["name"] == sample_item["name"]

    def test_update_item_not_found(self, client):
        response = client.put("/items/99999", json={"name": "Test"})
        assert response.status_code == 404

    def test_update_item_empty_body(self, client, sample_item):
        create_response = client.post("/items", json=sample_item)
        item_id = create_response.json()["data"]["id"]
        
        response = client.put(f"/items/{item_id}", json={})
        assert response.status_code == 200


class TestDeleteItem:
    def test_delete_item_success(self, client, sample_item):
        create_response = client.post("/items", json=sample_item)
        item_id = create_response.json()["data"]["id"]
        
        response = client.delete(f"/items/{item_id}")
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert data["message"] == "Item deleted successfully"
        
        get_response = client.get(f"/items/{item_id}")
        assert get_response.status_code == 404

    def test_delete_item_not_found(self, client):
        response = client.delete("/items/99999")
        assert response.status_code == 404
