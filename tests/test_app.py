from fastapi.testclient import TestClient

from src.app import activities, app


client = TestClient(app)


def test_unregister_participant_removes_their_email():
    activity_name = "Chess Club"
    email = "michael@mergington.edu"

    try:
        response = client.delete(
            f"/activities/{activity_name}/unregister",
            params={"email": email},
        )

        assert response.status_code == 200
        assert email not in activities[activity_name]["participants"]
    finally:
        if email not in activities[activity_name]["participants"]:
            activities[activity_name]["participants"].append(email)


def test_unregister_participant_returns_error_for_unknown_email():
    activity_name = "Chess Club"
    email = "missing@mergington.edu"

    response = client.delete(
        f"/activities/{activity_name}/unregister",
        params={"email": email},
    )

    assert response.status_code == 400


def test_activities_endpoint_disables_caching():
    response = client.get("/activities")

    assert response.status_code == 200
    assert response.headers["cache-control"].startswith("no-store")
