"""
validators.py — Input validation logic
"""

import re
from datetime import datetime


def validate_name(name: str, field: str) -> str | None:
    """Return error string or None if valid."""
    name = name.strip()
    if not name:
        return f"{field} is required."
    if len(name) < 2:
        return f"{field} must be at least 2 characters."
    if not re.match(r"^[A-Za-zÀ-ÿ\s\-']+$", name):
        return f"{field} must contain only letters."
    return None


def validate_birth_date(date_str: str) -> str | None:
    """Validate DD/MM/YYYY format and reasonable range."""
    date_str = date_str.strip()
    if not date_str:
        return "Birth Date is required."
    try:
        dt = datetime.strptime(date_str, "%d/%m/%Y")
        if dt.year < 1900 or dt > datetime.now():
            return "Birth Date must be between 1900 and today."
    except ValueError:
        return "Birth Date must be in DD/MM/YYYY format."
    return None


def validate_birth_place(place: str) -> str | None:
    place = place.strip()
    if not place:
        return "Birth Place is required."
    if len(place) < 2:
        return "Birth Place must be at least 2 characters."
    return None


def validate_phone(phone: str) -> str | None:
    """Accept formats: +213XXXXXXXXX, 0XXXXXXXXX, or 10+ digit numbers."""
    phone = phone.strip()
    if not phone:
        return "Phone Number is required."
    cleaned = re.sub(r"[\s\-\(\)]", "", phone)
    if not re.match(r"^(\+?\d{8,15})$", cleaned):
        return "Phone Number must be 8–15 digits (may start with +)."
    return None


def validate_all_fields(data: dict) -> list[str]:
    """
    Validate all user fields at once.
    Returns a list of error messages (empty list = all valid).
    """
    errors = []
    for check in [
        validate_name(data.get("first_name", ""), "First Name"),
        validate_name(data.get("last_name", ""), "Last Name"),
        validate_birth_date(data.get("birth_date", "")),
        validate_birth_place(data.get("birth_place", "")),
        validate_phone(data.get("phone", "")),
    ]:
        if check:
            errors.append(check)
    return errors
