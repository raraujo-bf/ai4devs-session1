from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_login_success_returns_token() -> None:
    response = client.post("/auth/login", json={"usuario": "admin", "password": "admin123"})

    assert response.status_code == 200
    body = response.json()
    assert body["token_type"] == "bearer"
    assert body["expires_in"] == 300
    assert body["access_token"]


def test_welcome_endpoint_requires_authentication() -> None:
    response = client.get("/api/me")

    assert response.status_code == 401


def test_me_returns_user_with_valid_token() -> None:
    login = client.post("/auth/login", json={"usuario": "admin", "password": "admin123"})
    token = login.json()["access_token"]
    bearer_prefix = "Bearer "

    response = client.get("/api/me", headers={"Authorization": bearer_prefix + token})

    assert response.status_code == 200
    assert response.json() == {"usuario": "admin"}
