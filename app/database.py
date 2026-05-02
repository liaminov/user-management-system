"""
database.py — MongoDB connection and CRUD operations
"""

import os
from pymongo import MongoClient, errors
from pymongo.collection import Collection
from bson import ObjectId
from dotenv import load_dotenv
from typing import Optional

load_dotenv()


def get_collection() -> Optional[Collection]:
    """Establish MongoDB connection and return the users collection."""
    try:
        uri = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
        db_name = os.getenv("DB_NAME", "user_management")
        col_name = os.getenv("COLLECTION_NAME", "users")

        client = MongoClient(uri, serverSelectionTimeoutMS=3000)
        client.server_info()  # trigger connection check
        db = client[db_name]
        col = db[col_name]

        # Ensure phone number uniqueness at the database level
        col.create_index("phone", unique=True)
        return col

    except errors.ServerSelectionTimeoutError:
        return None


# ──────────────────────────────────────────────
# CREATE
# ──────────────────────────────────────────────
def add_user(collection: Collection, user: dict) -> dict:
    """
    Insert a new user document.
    Returns {"ok": True, "id": inserted_id} or {"ok": False, "error": msg}.
    """
    try:
        result = collection.insert_one(user)
        return {"ok": True, "id": str(result.inserted_id)}
    except errors.DuplicateKeyError:
        return {"ok": False, "error": "Phone number already exists."}
    except Exception as e:
        return {"ok": False, "error": str(e)}


# ──────────────────────────────────────────────
# READ
# ──────────────────────────────────────────────
def get_all_users(collection: Collection) -> list:
    """Return all user documents as a list of dicts."""
    users = list(collection.find({}))
    for u in users:
        u["_id"] = str(u["_id"])
    return users


def search_users(collection: Collection, query: str) -> list:
    """
    Case-insensitive search across all text fields.
    Returns matching documents.
    """
    if not query.strip():
        return get_all_users(collection)

    regex = {"$regex": query, "$options": "i"}
    filters = {
        "$or": [
            {"first_name": regex},
            {"last_name": regex},
            {"birth_place": regex},
            {"phone": regex},
            {"birth_date": regex},
        ]
    }
    users = list(collection.find(filters))
    for u in users:
        u["_id"] = str(u["_id"])
    return users


# ──────────────────────────────────────────────
# UPDATE
# ──────────────────────────────────────────────
def update_user(collection: Collection, user_id: str, updated: dict) -> dict:
    """
    Update a user by their ObjectId string.
    Returns {"ok": True} or {"ok": False, "error": msg}.
    """
    try:
        result = collection.update_one(
            {"_id": ObjectId(user_id)},
            {"$set": updated}
        )
        if result.matched_count == 0:
            return {"ok": False, "error": "User not found."}
        return {"ok": True}
    except errors.DuplicateKeyError:
        return {"ok": False, "error": "Phone number already in use by another user."}
    except Exception as e:
        return {"ok": False, "error": str(e)}


# ──────────────────────────────────────────────
# DELETE
# ──────────────────────────────────────────────
def delete_user(collection: Collection, user_id: str) -> dict:
    """
    Delete a user by their ObjectId string.
    Returns {"ok": True} or {"ok": False, "error": msg}.
    """
    try:
        result = collection.delete_one({"_id": ObjectId(user_id)})
        if result.deleted_count == 0:
            return {"ok": False, "error": "User not found."}
        return {"ok": True}
    except Exception as e:
        return {"ok": False, "error": str(e)}
