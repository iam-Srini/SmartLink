from fastapi import status
from app.models.user import User
from app.models.link import Link


def test_create_link_endpoint(client, test_user):
    """Test creating a shortened link for a logged-in user."""
    login_response = client.post(
        "/users/login",
        data={"username": test_user.email, "password": "Test@12345"},
    )
    assert login_response.status_code == 200

    token = login_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    payload = {"original_url": "https://example.com"}
    response = client.post("/links/", json=payload, headers=headers)
    data = response.json()

    assert response.status_code == status.HTTP_200_OK
    assert data["original_url"] == "https://example.com/"
    assert "short_url" in data


def test_get_short_url(client, db_session):
    """Test retrieving a short URL and ensuring it redirects correctly."""
    user = db_session.query(User).filter(User.email == "testuser@gmail.com").first()
    link = db_session.query(Link).filter(Link.user_id == user.id).first()

    response = client.get(f"/links/{link.short_url}", follow_redirects=False)
    assert response.is_redirect
    assert response.headers["location"] == link.original_url


def test_create_multiple_links(client):
    """Test creating multiple links for the same user."""
    login_response = client.post(
        "/users/login",
        data={"username": "testuser@gmail.com", "password": "Test@12345"},
    )
    assert login_response.status_code == 200

    token = login_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    payload = {"original_url": "https://www.yahoo.com"}
    response = client.post("/links/", json=payload, headers=headers)

    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["original_url"] == "https://www.yahoo.com/"
    assert "short_url" in data
