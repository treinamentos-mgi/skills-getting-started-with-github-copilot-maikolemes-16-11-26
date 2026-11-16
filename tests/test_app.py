def test_root_redirects_to_static_index(client):
    response = client.get("/", follow_redirects=False)

    assert response.status_code == 307
    assert response.headers["location"] == "/static/index.html"


def test_get_activities_returns_activity_details(client):
    response = client.get("/activities")

    assert response.status_code == 200
    activities = response.json()
    assert "Aulas de cerâmica" in activities
    assert activities["Aulas de cerâmica"]["participants"] == []
    assert activities["Aulas de cerâmica"]["max_participants"] == 20


def test_signup_adds_participant_to_activity(client):
    activity_name = "Aulas de cerâmica"
    email = "student@example.com"

    response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": email},
    )

    assert response.status_code == 200
    assert response.json()["message"] == f"Signed up {email} for {activity_name}"

    activities_response = client.get("/activities")
    assert email in activities_response.json()[activity_name]["participants"]


def test_signup_rejects_duplicate_participant(client):
    response = client.post(
        "/activities/Programming Class/signup",
        params={"email": "emma@mergington.edu"},
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "Estudante já inscrito nesta atividade"


def test_signup_rejects_unknown_activity(client):
    response = client.post(
        "/activities/Unknown Activity/signup",
        params={"email": "student@example.com"},
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_cancel_signup_removes_participant_from_activity(client):
    activity_name = "Chess Club"
    email = "michael@mergington.edu"

    response = client.delete(
        f"/activities/{activity_name}/signup",
        params={"email": email},
    )

    assert response.status_code == 200
    assert response.json()["message"] == f"Cancelled signup for {email} in {activity_name}"

    activities_response = client.get("/activities")
    assert email not in activities_response.json()[activity_name]["participants"]


def test_cancel_signup_rejects_unregistered_participant(client):
    response = client.delete(
        "/activities/Aulas de cerâmica/signup",
        params={"email": "student@example.com"},
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Estudante não inscrito nesta atividade"


def test_cancel_signup_rejects_unknown_activity(client):
    response = client.delete(
        "/activities/Unknown Activity/signup",
        params={"email": "student@example.com"},
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"
