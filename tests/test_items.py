def test_create_and_list_items(client):
    resp = client.post(
        "/items/",
        json={"name": "Ski", "description": "Slalom skis", "category": "Winter Sports"},
    )
    assert resp.status_code == 201
    data = resp.get_json()
    assert data["name"] == "Ski"
    assert data["available"] is True

    resp = client.get("/items/")
    assert resp.status_code == 200
    assert len(resp.get_json()) == 1


def test_create_item_missing_name(client):
    resp = client.post("/items/", json={"description": "No name"})
    assert resp.status_code == 400


def test_get_item(client):
    create = client.post("/items/", json={"name": "Sykkel"})
    item_id = create.get_json()["id"]
    resp = client.get(f"/items/{item_id}")
    assert resp.status_code == 200
    assert resp.get_json()["name"] == "Sykkel"


def test_get_item_not_found(client):
    resp = client.get("/items/999")
    assert resp.status_code == 404


def test_update_item(client):
    create = client.post("/items/", json={"name": "Fotball"})
    item_id = create.get_json()["id"]
    resp = client.put(f"/items/{item_id}", json={"description": "Size 5 football"})
    assert resp.status_code == 200
    assert resp.get_json()["description"] == "Size 5 football"


def test_delete_item(client):
    create = client.post("/items/", json={"name": "Telt"})
    item_id = create.get_json()["id"]
    resp = client.delete(f"/items/{item_id}")
    assert resp.status_code == 204


def test_filter_available_items(client):
    client.post("/items/", json={"name": "Ryggsekk"})
    resp = client.get("/items/?available=true")
    assert resp.status_code == 200
    items = resp.get_json()
    assert all(i["available"] for i in items)
