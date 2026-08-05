def _register_and_login(client, email="tasker@example.com", password="supersecret1"):
    client.post("/api/v1/auth/register", json={"email": email, "password": password})
    login_response = client.post(
        "/api/v1/auth/login", data={"username": email, "password": password}
    )
    token = login_response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


def test_create_and_list_tasks(client):
    headers = _register_and_login(client)

    create_response = client.post(
        "/api/v1/tasks",
        json={"title": "Write portfolio README", "description": "Explain the stack"},
        headers=headers,
    )
    assert create_response.status_code == 201
    task = create_response.json()
    assert task["title"] == "Write portfolio README"
    assert task["status"] == "todo"

    list_response = client.get("/api/v1/tasks", headers=headers)
    assert list_response.status_code == 200
    assert len(list_response.json()) == 1


def test_update_task_status(client):
    headers = _register_and_login(client)
    task = client.post(
        "/api/v1/tasks", json={"title": "Dockerize backend"}, headers=headers
    ).json()

    update_response = client.put(
        f"/api/v1/tasks/{task['id']}",
        json={"status": "done"},
        headers=headers,
    )
    assert update_response.status_code == 200
    assert update_response.json()["status"] == "done"


def test_delete_task(client):
    headers = _register_and_login(client)
    task = client.post(
        "/api/v1/tasks", json={"title": "Temporary task"}, headers=headers
    ).json()

    delete_response = client.delete(f"/api/v1/tasks/{task['id']}", headers=headers)
    assert delete_response.status_code == 204

    get_response = client.get(f"/api/v1/tasks/{task['id']}", headers=headers)
    assert get_response.status_code == 404


def test_tasks_are_isolated_per_user(client):
    headers_a = _register_and_login(client, email="user-a@example.com")
    headers_b = _register_and_login(client, email="user-b@example.com")

    client.post("/api/v1/tasks", json={"title": "User A's task"}, headers=headers_a)

    response_b = client.get("/api/v1/tasks", headers=headers_b)
    assert response_b.status_code == 200
    assert response_b.json() == []


def test_unauthenticated_request_rejected(client):
    response = client.get("/api/v1/tasks")
    assert response.status_code == 401
