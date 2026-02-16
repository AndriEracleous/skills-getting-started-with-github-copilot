import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert data  # Should not be empty

def test_signup_and_unregister():
    # Get an activity name
    activities = client.get("/activities").json()
    activity_name = next(iter(activities))
    test_email = "pytestuser@mergington.edu"

    # Sign up
    signup_resp = client.post(f"/activities/{activity_name}/signup", params={"email": test_email})
    assert signup_resp.status_code == 200
    assert "message" in signup_resp.json()

    # Duplicate signup should fail or return error
    dup_resp = client.post(f"/activities/{activity_name}/signup", params={"email": test_email})
    assert dup_resp.status_code != 200 or "detail" in dup_resp.json()

    # Unregister
    unregister_resp = client.post(f"/activities/{activity_name}/unregister", params={"email": test_email})
    assert unregister_resp.status_code == 200
    assert "message" in unregister_resp.json()

    # Unregister again should fail or return error
    unregister_again = client.post(f"/activities/{activity_name}/unregister", params={"email": test_email})
    assert unregister_again.status_code != 200 or "detail" in unregister_again.json()
