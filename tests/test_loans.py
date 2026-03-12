def _setup(client):
    """Helper: create a user and an item, return their IDs."""
    user_id = client.post(
        "/users/", json={"name": "Test User", "email": "test@example.com"}
    ).get_json()["id"]
    item_id = client.post(
        "/items/", json={"name": "Kano", "category": "Water Sports"}
    ).get_json()["id"]
    return user_id, item_id


def test_create_and_list_loans(client):
    user_id, item_id = _setup(client)
    resp = client.post("/loans/", json={"user_id": user_id, "item_id": item_id})
    assert resp.status_code == 201
    data = resp.get_json()
    assert data["is_active"] is True

    resp = client.get("/loans/")
    assert resp.status_code == 200
    assert len(resp.get_json()) == 1


def test_create_loan_item_unavailable(client):
    user_id, item_id = _setup(client)
    client.post("/loans/", json={"user_id": user_id, "item_id": item_id})
    resp = client.post("/loans/", json={"user_id": user_id, "item_id": item_id})
    assert resp.status_code == 409


def test_create_loan_missing_fields(client):
    resp = client.post("/loans/", json={"user_id": 1})
    assert resp.status_code == 400


def test_return_loan(client):
    user_id, item_id = _setup(client)
    loan_id = client.post(
        "/loans/", json={"user_id": user_id, "item_id": item_id}
    ).get_json()["id"]

    resp = client.post(f"/loans/{loan_id}/return")
    assert resp.status_code == 200
    assert resp.get_json()["is_active"] is False

    item_resp = client.get(f"/items/{item_id}")
    assert item_resp.get_json()["available"] is True


def test_return_loan_already_returned(client):
    user_id, item_id = _setup(client)
    loan_id = client.post(
        "/loans/", json={"user_id": user_id, "item_id": item_id}
    ).get_json()["id"]
    client.post(f"/loans/{loan_id}/return")
    resp = client.post(f"/loans/{loan_id}/return")
    assert resp.status_code == 409


def test_filter_active_loans(client):
    user_id, item_id = _setup(client)
    loan_id = client.post(
        "/loans/", json={"user_id": user_id, "item_id": item_id}
    ).get_json()["id"]
    client.post(f"/loans/{loan_id}/return")

    resp = client.get("/loans/?active=true")
    assert resp.status_code == 200
    assert len(resp.get_json()) == 0


def test_get_loan_not_found(client):
    resp = client.get("/loans/999")
    assert resp.status_code == 404


def test_loan_with_due_date(client):
    user_id, item_id = _setup(client)
    resp = client.post(
        "/loans/",
        json={
            "user_id": user_id,
            "item_id": item_id,
            "due_date": "2026-04-01T12:00:00",
        },
    )
    assert resp.status_code == 201
    assert resp.get_json()["due_date"] is not None


def test_loan_invalid_due_date(client):
    user_id, item_id = _setup(client)
    resp = client.post(
        "/loans/",
        json={"user_id": user_id, "item_id": item_id, "due_date": "not-a-date"},
    )
    assert resp.status_code == 400
