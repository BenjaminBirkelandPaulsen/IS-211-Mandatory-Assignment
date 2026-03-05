import pytest


def test_create_and_list_users(client):
    resp = client.post(
        "/users/", json={"name": "Kari Nordmann", "email": "kari@example.com"}
    )
    assert resp.status_code == 201
    data = resp.get_json()
    assert data["name"] == "Kari Nordmann"
    assert data["email"] == "kari@example.com"

    resp = client.get("/users/")
    assert resp.status_code == 200
    users = resp.get_json()
    assert len(users) == 1
    assert users[0]["email"] == "kari@example.com"


def test_create_user_missing_fields(client):
    resp = client.post("/users/", json={"name": "Ola"})
    assert resp.status_code == 400


def test_create_user_duplicate_email(client):
    client.post("/users/", json={"name": "A", "email": "a@example.com"})
    resp = client.post("/users/", json={"name": "B", "email": "a@example.com"})
    assert resp.status_code == 409


def test_get_user(client):
    create = client.post(
        "/users/", json={"name": "Ola", "email": "ola@example.com", "phone": "12345678"}
    )
    user_id = create.get_json()["id"]
    resp = client.get(f"/users/{user_id}")
    assert resp.status_code == 200
    assert resp.get_json()["phone"] == "12345678"


def test_get_user_not_found(client):
    resp = client.get("/users/999")
    assert resp.status_code == 404


def test_delete_user(client):
    create = client.post(
        "/users/", json={"name": "Del", "email": "del@example.com"}
    )
    user_id = create.get_json()["id"]
    resp = client.delete(f"/users/{user_id}")
    assert resp.status_code == 204
    assert client.get(f"/users/{user_id}").status_code == 404
