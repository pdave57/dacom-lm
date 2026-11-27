from fastapi.testclient import TestClient


def test_register_returns_tokens(client: TestClient) -> None:
    response = client.post(
        "/api/v1/auth/register",
        json={
            "email": "learner@dacom.dev",
            "password": "strongpassword123",
            "full_name": "Test Learner",
        },
    )
    assert response.status_code == 201
    data = response.json()
    assert "access_token" in data
    assert "refresh_token" in data
    assert data["token_type"] == "bearer"
