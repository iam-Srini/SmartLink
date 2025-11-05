from fastapi import status
from unittest.mock import patch, ANY


def test_user_register(client):
    """Test user registration and OTP email sending."""
    with patch("app.routers.users.send_otp_email") as mock_send_email:
        mock_send_email.return_value = None

        payload = {
            "username": "user1",
            "email": "user1@example.com",
            "password": "Strong@123",
        }

        response = client.post(url="/users/register", json=payload)
        assert response.status_code == status.HTTP_200_OK

        data = response.json()
        assert data["email"] == "user1@example.com"

        mock_send_email.assert_called_once_with(
            ANY,
            "user1@example.com",
            data["otp_code"] if "otp_code" in data else ANY,
        )


def test_verify_user(client, db_session):
    """Test user email verification using OTP."""
    from app.models.user import User

    user_data = db_session.query(User).filter(User.email == "user1@example.com").first()
    otp_code = user_data.otp_code

    verify_user_payload = {
        "email": "user1@example.com",
        "otp": otp_code,
    }

    response = client.post(url="/users/verify-email", params=verify_user_payload)
    data = response.json()
    assert response.status_code == status.HTTP_200_OK


def test_login_user(client, db_session):
    """Test login for a verified user and check returned access token."""
    form_data = {
        "username": "user1@example.com",
        "password": "Strong@123",
    }

    response = client.post(url="/users/login", data=form_data)
    data = response.json()

    assert response.status_code == status.HTTP_200_OK
    assert "access_token" in data
    assert data["token_type"] == "bearer"
    assert isinstance(data["access_token"], str)
    assert len(data["access_token"]) > 10


def test_login_user_invalid_password(client):
    """Test login failure with incorrect password."""
    form_data = {
        "username": "user1@example.com",
        "password": "WrongPassword123",
    }

    response = client.post("/users/login", data=form_data)
    data = response.json()

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert "Incorrect email or password." in data["detail"]
