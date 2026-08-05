def test_register_user(client):
    response = client.post(
        "/api/v1/auth/register",
        json={"email": "alice@example.com", "password": "supersecret1"},
    )
    assert response.status_code == 201
    body = response.json()
    assert body["email"] == "alice@example.com"
    assert "hashed_password" not in body  # never leak the hash


def test_register_duplicate_email_fails(client):
    payload = {"email": "bob@example.com", "password": "supersecret1"}
    client.post("/api/v1/auth/register", json=payload)
    response = client.post("/api/v1/auth/register", json=payload)
    assert response.status_code == 400


def test_login_success(client):
    client.post(
        "/api/v1/auth/register",
        json={"email": "carol@example.com", "password": "supersecret1"},
    )
    response = client.post(
        "/api/v1/auth/login",
        data={"username": "carol@example.com", "password": "supersecret1"},
    )
    assert response.status_code == 200
    body = response.json()
    assert body["token_type"] == "bearer"
    assert body["access_token"]


def test_login_wrong_password_fails(client):
    client.post(
        "/api/v1/auth/register",
        json={"email": "dave@example.com", "password": "supersecret1"},
    )
    response = client.post(
        "/api/v1/auth/login",
        data={"username": "dave@example.com", "password": "wrongpass"},
    )
    assert response.status_code == 401
