def test_register_success(client):
    r = client.post("/api/user/register", json={
        "name": "Alice", "email": "alice@example.com", "password": "secret123"})
    assert r.status_code == 200
    assert r.json()["message"] == "註冊成功"


def test_register_duplicate_email(client):
    p = {"name": "Bob", "email": "bob@example.com", "password": "secret123"}
    assert client.post("/api/user/register", json=p).status_code == 200
    assert client.post("/api/user/register", json=p).status_code == 400


def test_register_invalid_email(client):
    r = client.post("/api/user/register", json={
        "name": "X", "email": "not-email", "password": "secret123"})
    assert r.status_code == 422


def test_login_success(client):
    client.post("/api/user/register", json={
        "name": "Carol", "email": "carol@example.com", "password": "secret123"})
    r = client.post("/api/user/login", json={
        "email": "carol@example.com", "password": "secret123"})
    assert r.status_code == 200
    assert r.json()["access_token"]
    assert r.json()["user"]["email"] == "carol@example.com"


def test_login_wrong_password(client):
    client.post("/api/user/register", json={
        "name": "Dave", "email": "dave@example.com", "password": "secret123"})
    assert client.post("/api/user/login", json={
        "email": "dave@example.com", "password": "WRONG"}).status_code == 400


def test_login_nonexistent(client):
    assert client.post("/api/user/login", json={
        "email": "ghost@example.com", "password": "x"}).status_code == 400


def test_me_requires_auth(client):
    assert client.get("/api/user/me").status_code == 401


def test_me_returns_current_user(client, auth_headers):
    r = client.get("/api/user/me", headers=auth_headers)
    assert r.status_code == 200
    assert r.json()["email"] == "tester@example.com"
