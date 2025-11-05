import random
from datetime import datetime, timedelta, timezone


def generate_otp() -> str:
    """
    Generate a 6-digit numeric OTP as a string.
    """
    return str(random.randint(100000, 999999))


def otp_expiry_time(minutes: int = 10) -> datetime:
    """
    Return the UTC expiration time for an OTP based on the given duration in minutes.
    """
    return datetime.now(timezone.utc) + timedelta(minutes=minutes)
