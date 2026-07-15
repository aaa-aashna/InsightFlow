from main import app


def test_health_endpoint(client):
    response = client.get("/health")
    assert response.status_code == 200
    payload = response.json()
    assert payload["status"] == "ok"


def test_analysis_endpoint_returns_structured_insights(client):
    response = client.post(
        "/api/v1/analysis",
        json={"text": "This is a powerful story about building a business from scratch."},
    )
    assert response.status_code == 200
    payload = response.json()
    assert payload["content_quality_score"] >= 0
    assert payload["virality_prediction"] in {"low", "medium", "high"}
    assert "recommended_hashtags" in payload


def test_register_and_login_flow(client):
    signup = client.post(
        "/api/v1/auth/register",
        json={"email": "creator@example.com", "password": "Secret123!", "full_name": "Test Creator"},
    )
    assert signup.status_code == 201

    login = client.post(
        "/api/v1/auth/login",
        json={"email": "creator@example.com", "password": "Secret123!"},
    )
    assert login.status_code == 200
    payload = login.json()
    assert "access_token" in payload
    assert "refresh_token" in payload
