def test_root_redirects_to_static_index(client):
    # Arrange
    path = "/"

    # Act
    response = client.get(path, follow_redirects=False)

    # Assert
    assert response.status_code == 307
    assert response.headers["location"] == "/static/index.html"

    follow_response = client.get(response.headers["location"])
    assert follow_response.status_code == 200


def test_get_activities_returns_activities(client):
    # Arrange

    # Act
    response = client.get("/activities")

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data


def test_signup_for_activity_adds_participant(client):
    # Arrange
    activity_name = "Chess Club"
    new_email = "teststudent@mergington.edu"
    params = {"email": new_email}

    # Act
    response = client.post(f"/activities/{activity_name}/signup", params=params)

    # Assert
    assert response.status_code == 200
    assert response.json() == {"message": f"Signed up {new_email} for {activity_name}"}

    activities = client.get("/activities").json()
    assert new_email in activities[activity_name]["participants"]


def test_signup_for_activity_duplicate_returns_400(client):
    # Arrange
    activity_name = "Chess Club"
    existing_email = "michael@mergington.edu"
    params = {"email": existing_email}

    # Act
    response = client.post(f"/activities/{activity_name}/signup", params=params)

    # Assert
    assert response.status_code == 400
    assert response.json()["detail"] == "Student already signed up for this activity"


def test_remove_participant_from_activity(client):
    # Arrange
    activity_name = "Programming Class"
    email = "removeme@mergington.edu"
    client.post(f"/activities/{activity_name}/signup", params={"email": email})

    # Act
    response = client.delete(f"/activities/{activity_name}/participants", params={"email": email})

    # Assert
    assert response.status_code == 200
    assert response.json() == {"message": f"Removed {email} from {activity_name}"}

    activities = client.get("/activities").json()
    assert email not in activities[activity_name]["participants"]


def test_remove_unknown_participant_returns_404(client):
    # Arrange
    activity_name = "Art Studio"
    params = {"email": "unknown@mergington.edu"}

    # Act
    response = client.delete(f"/activities/{activity_name}/participants", params=params)

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Participant not found in activity"
