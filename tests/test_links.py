from fastapi import status
from app.models.user import User
from app.models.link import Link

def test_create_link_endpoint(client, test_user):
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
    print(data)
    assert response.status_code == status.HTTP_200_OK

def test_get_short_url(client, db_session):
    user = db_session.query(User).filter(User.email == "testuser@gmail.com").first()
    link = db_session.query(Link).filter(Link.user_id == user.id).first()
    print(link.short_url)
    response = client.get(f"/links/{link.short_url}", follow_redirects=False)
    print(response.headers['location'])
    assert response.is_redirect

def test_create_multiple_links(client):
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

