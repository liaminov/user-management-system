# 👤 Advanced User Management System

A full-featured **User Management System** built with **Python · Streamlit · MongoDB**.
Implements complete CRUD operations through a polished GUI.

---

## 🗂️ Project Structure

```
user_management/
├── app/
│   ├── main.py          # Streamlit GUI (entry point)
│   ├── database.py      # MongoDB CRUD operations
│   └── validators.py    # Input validation logic
├── tests/
│   └── test_validators.py
├── .env.example         # Environment variable template
├── requirements.txt
└── README.md
```

---

## ⚙️ Setup & Installation

### 1. Clone the repository
```bash
git clone https://github.com/<your-username>/user-management-system.git
cd user-management-system
```

### 2. Create and activate a virtual environment
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS / Linux
source venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure environment variables
```bash
cp .env.example .env
# Edit .env with your MongoDB connection string
```

`.env` file:
```
MONGO_URI=mongodb://localhost:27017/
DB_NAME=user_management
COLLECTION_NAME=users
```

### 5. Start MongoDB
```bash
# If installed locally
mongod

# Or use MongoDB Atlas (cloud) — update MONGO_URI in .env accordingly
```

### 6. Run the application
```bash
streamlit run app/main.py
```

The app opens automatically at **http://localhost:8501**

---

## 🧪 Running Tests

```bash
python -m pytest tests/ -v
```

---

## ✨ Features

| Feature | Description |
|---|---|
| ➕ Add User | Form with full validation before DB insertion |
| 📋 Display Users | Searchable table fetched live from MongoDB |
| 🔍 Search | Real-time across all fields |
| ✏️ Edit User | Load → modify → save back to DB |
| 🗑️ Delete User | Confirmation prompt before deletion |
| ✅ Validation | Empty fields, date format, unique phone |
| ⚠️ Error Handling | DB connection errors, duplicate phone, not found |

---

## 🗃️ MongoDB Document Structure

```json
{
  "_id": "ObjectId(...)",
  "first_name": "Amina",
  "last_name": "Benali",
  "birth_date": "10/03/1998",
  "birth_place": "Algiers",
  "phone": "+213551234567"
}
```

---

## 🌿 Git Branching Strategy

```
main          ← production-ready, stable
develop       ← integration branch
feature/gui       ← Streamlit interface
feature/database  ← MongoDB integration
feature/validation← input validation
```

---

## 👥 Team

| Member | Branch | Role |
|---|---|---|
| Student 1 | feature/gui | GUI development |
| Student 2 | feature/database | DB integration |
| Student 3 | feature/validation | Validation & tests |

---

## 📄 License
MIT License — see `LICENSE` for details.
