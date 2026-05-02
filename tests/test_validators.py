"""
test_validators.py — Unit tests for the validators module
Run with: python -m pytest tests/ -v
"""

import pytest
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from app.validators import (
    validate_name,
    validate_birth_date,
    validate_birth_place,
    validate_phone,
    validate_all_fields,
)


# ──────────────────────────────────────────────
# validate_name
# ──────────────────────────────────────────────
class TestValidateName:
    def test_valid_name(self):
        assert validate_name("Amina", "First Name") is None

    def test_valid_name_with_hyphen(self):
        assert validate_name("Jean-Pierre", "First Name") is None

    def test_empty_name(self):
        assert validate_name("", "First Name") is not None

    def test_too_short(self):
        assert validate_name("A", "First Name") is not None

    def test_numbers_in_name(self):
        assert validate_name("John2", "Last Name") is not None

    def test_accented_chars(self):
        assert validate_name("Léa", "First Name") is None


# ──────────────────────────────────────────────
# validate_birth_date
# ──────────────────────────────────────────────
class TestValidateBirthDate:
    def test_valid_date(self):
        assert validate_birth_date("15/06/1995") is None

    def test_empty_date(self):
        assert validate_birth_date("") is not None

    def test_wrong_format(self):
        assert validate_birth_date("1995-06-15") is not None

    def test_future_date(self):
        assert validate_birth_date("01/01/2099") is not None

    def test_year_before_1900(self):
        assert validate_birth_date("01/01/1800") is not None

    def test_invalid_day(self):
        assert validate_birth_date("32/01/2000") is not None


# ──────────────────────────────────────────────
# validate_birth_place
# ──────────────────────────────────────────────
class TestValidateBirthPlace:
    def test_valid_place(self):
        assert validate_birth_place("Algiers") is None

    def test_empty_place(self):
        assert validate_birth_place("") is not None

    def test_too_short(self):
        assert validate_birth_place("A") is not None


# ──────────────────────────────────────────────
# validate_phone
# ──────────────────────────────────────────────
class TestValidatePhone:
    def test_valid_international(self):
        assert validate_phone("+213551234567") is None

    def test_valid_local(self):
        assert validate_phone("0551234567") is None

    def test_empty_phone(self):
        assert validate_phone("") is not None

    def test_too_short(self):
        assert validate_phone("123") is not None

    def test_letters_in_phone(self):
        assert validate_phone("055ABC1234") is not None

    def test_spaces_accepted(self):
        # spaces are stripped before matching
        assert validate_phone("0551 234 567") is None


# ──────────────────────────────────────────────
# validate_all_fields
# ──────────────────────────────────────────────
class TestValidateAllFields:
    def test_all_valid(self):
        data = {
            "first_name":  "Amina",
            "last_name":   "Benali",
            "birth_date":  "10/03/1998",
            "birth_place": "Algiers",
            "phone":       "+213551234567",
        }
        assert validate_all_fields(data) == []

    def test_multiple_errors(self):
        data = {
            "first_name":  "",
            "last_name":   "",
            "birth_date":  "not-a-date",
            "birth_place": "",
            "phone":       "",
        }
        errors = validate_all_fields(data)
        assert len(errors) == 5

    def test_partial_errors(self):
        data = {
            "first_name":  "Amina",
            "last_name":   "Benali",
            "birth_date":  "bad",
            "birth_place": "Oran",
            "phone":       "+213551234567",
        }
        errors = validate_all_fields(data)
        assert len(errors) == 1
        assert "Birth Date" in errors[0]
