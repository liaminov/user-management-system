"""
main.py — Streamlit GUI for the Advanced User Management System
Run with: streamlit run app/main.py
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

import streamlit as st
import pandas as pd
from app.database import (
    get_collection, add_user, get_all_users,
    search_users, update_user, delete_user
)
from app.validators import validate_all_fields

# ──────────────────────────────────────────────
# PAGE CONFIG & GLOBAL STYLE
# ──────────────────────────────────────────────
st.set_page_config(
    page_title="User Management System",
    page_icon="👤",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
/* ── Google Font ── */
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;600&display=swap');

/* ── Root variables ── */
:root {
    --bg:        #0b0f19;
    --surface:   #111827;
    --border:    #1f2d45;
    --accent:    #3b82f6;
    --accent2:   #06b6d4;
    --danger:    #ef4444;
    --success:   #22c55e;
    --warn:      #f59e0b;
    --text:      #e2e8f0;
    --muted:     #64748b;
    --radius:    12px;
}

/* ── Base ── */
html, body, [class*="css"] {
    font-family: 'Space Grotesk', sans-serif !important;
    background-color: var(--bg) !important;
    color: var(--text) !important;
}

/* ── Hide Streamlit chrome ── */
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 2rem 2.5rem 3rem !important; max-width: 1400px; }

/* ── Hero header ── */
.hero {
    background: linear-gradient(135deg, #0f172a 0%, #1e3a5f 50%, #0f172a 100%);
    border: 1px solid var(--border);
    border-radius: 16px;
    padding: 2rem 2.5rem;
    margin-bottom: 2rem;
    position: relative;
    overflow: hidden;
}
.hero::before {
    content: '';
    position: absolute;
    top: -50%;
    right: -10%;
    width: 400px;
    height: 400px;
    background: radial-gradient(circle, rgba(59,130,246,0.12) 0%, transparent 70%);
    pointer-events: none;
}
.hero h1 {
    font-size: 2rem !important;
    font-weight: 700 !important;
    background: linear-gradient(90deg, #60a5fa, #22d3ee);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin: 0 0 0.25rem !important;
}
.hero p { color: var(--muted); margin: 0; font-size: 0.95rem; }

/* ── Section cards ── */
.card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: var(--radius);
    padding: 1.5rem;
    margin-bottom: 1.5rem;
}
.card-title {
    font-size: 0.75rem;
    font-weight: 600;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: var(--accent);
    margin-bottom: 1.25rem;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}

/* ── Inputs ── */
.stTextInput > div > div > input,
.stDateInput > div > div > input,
.stSelectbox > div > div {
    background: #0b0f19 !important;
    border: 1px solid var(--border) !important;
    border-radius: 8px !important;
    color: var(--text) !important;
    font-family: 'Space Grotesk', sans-serif !important;
}
.stTextInput > div > div > input:focus {
    border-color: var(--accent) !important;
    box-shadow: 0 0 0 3px rgba(59,130,246,0.15) !important;
}
label { color: var(--muted) !important; font-size: 0.8rem !important; font-weight: 500 !important; }

/* ── Buttons ── */
.stButton > button {
    border-radius: 8px !important;
    font-weight: 600 !important;
    font-family: 'Space Grotesk', sans-serif !important;
    transition: all 0.2s ease !important;
    border: none !important;
    width: 100%;
}
.stButton > button:hover { transform: translateY(-1px) !important; }

/* Primary */
div[data-testid="column"]:nth-child(1) .stButton > button {
    background: linear-gradient(135deg, #2563eb, #3b82f6) !important;
    color: white !important;
}
/* Danger */
div[data-testid="column"]:nth-child(2) .stButton > button {
    background: linear-gradient(135deg, #dc2626, #ef4444) !important;
    color: white !important;
}

/* ── Table ── */
.stDataFrame { border-radius: var(--radius) !important; overflow: hidden !important; }
.stDataFrame [data-testid="stDataFrameResizable"] {
    background: var(--surface) !important;
}

/* ── Alerts ── */
.stSuccess { background: rgba(34,197,94,0.1) !important; border-left: 3px solid var(--success) !important; border-radius: 8px !important; }
.stError   { background: rgba(239,68,68,0.1)  !important; border-left: 3px solid var(--danger)  !important; border-radius: 8px !important; }
.stWarning { background: rgba(245,158,11,0.1) !important; border-left: 3px solid var(--warn)    !important; border-radius: 8px !important; }
.stInfo    { background: rgba(59,130,246,0.1) !important; border-left: 3px solid var(--accent)  !important; border-radius: 8px !important; }

/* ── Stats badge ── */
.stat-badge {
    background: linear-gradient(135deg, #1e3a5f, #1e293b);
    border: 1px solid var(--border);
    border-radius: 10px;
    padding: 1rem 1.25rem;
    text-align: center;
}
.stat-badge .val {
    font-size: 2rem;
    font-weight: 700;
    background: linear-gradient(90deg, #60a5fa, #22d3ee);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}
.stat-badge .lbl { font-size: 0.75rem; color: var(--muted); font-weight: 500; }

/* ── Search bar ── */
.search-wrap .stTextInput > div > div > input {
    font-size: 1rem !important;
    padding: 0.75rem 1rem !important;
}

/* ── Divider ── */
hr { border-color: var(--border) !important; margin: 1.5rem 0 !important; }

/* ── Connection indicator ── */
.conn-ok  { color: var(--success); font-weight: 600; }
.conn-err { color: var(--danger);  font-weight: 600; }
</style>
""", unsafe_allow_html=True)


# ──────────────────────────────────────────────
# SESSION STATE
# ──────────────────────────────────────────────
def init_state():
    defaults = {
        "edit_id":    None,
        "edit_data":  {},
        "confirm_del": None,
        "search_q":   "",
        "refresh":    0,
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

init_state()


# ──────────────────────────────────────────────
# DATABASE CONNECTION
# ──────────────────────────────────────────────
@st.cache_resource(show_spinner=False)
def connect():
    return get_collection()

col = connect()


# ──────────────────────────────────────────────
# HERO
# ──────────────────────────────────────────────
st.markdown("""
<div class="hero">
    <h1>👤 User Management System</h1>
    <p>Advanced CRUD · MongoDB · Streamlit · Python</p>
</div>
""", unsafe_allow_html=True)

# Connection status
if col is None:
    st.error("⚠️ **MongoDB connection failed.** Please check your `.env` file and ensure MongoDB is running.")
    st.code("""
# .env
MONGO_URI=mongodb://localhost:27017/
DB_NAME=user_management
COLLECTION_NAME=users
    """, language="bash")
    st.stop()


# ──────────────────────────────────────────────
# STATS ROW
# ──────────────────────────────────────────────
all_users = get_all_users(col)
total = len(all_users)

s1, s2, s3, s4 = st.columns(4)
stats = [
    (s1, "👥", total, "Total Users"),
    (s2, "✅", "Live",   "DB Status"),
    (s3, "🗄️", col.database.name, "Database"),
    (s4, "📦", col.name, "Collection"),
]
for container, icon, val, label in stats:
    with container:
        st.markdown(f"""
        <div class="stat-badge">
            <div class="val">{icon} {val}</div>
            <div class="lbl">{label}</div>
        </div>
        """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)


# ──────────────────────────────────────────────
# LAYOUT: LEFT = FORM  |  RIGHT = TABLE
# ──────────────────────────────────────────────
left, right = st.columns([1, 2], gap="large")


# ══════════════════════════════════════════════
# LEFT PANEL — ADD / EDIT FORM
# ══════════════════════════════════════════════
with left:
    is_edit = st.session_state.edit_id is not None
    title   = "✏️ EDIT USER" if is_edit else "➕ ADD NEW USER"

    st.markdown(f'<div class="card-title">{title}</div>', unsafe_allow_html=True)

    ed = st.session_state.edit_data

    with st.form("user_form", clear_on_submit=not is_edit):
        first_name  = st.text_input("First Name",   value=ed.get("first_name", ""),  placeholder="e.g. Amina")
        last_name   = st.text_input("Last Name",    value=ed.get("last_name", ""),   placeholder="e.g. Benali")
        birth_date  = st.text_input("Birth Date",   value=ed.get("birth_date", ""),  placeholder="DD/MM/YYYY")
        birth_place = st.text_input("Birth Place",  value=ed.get("birth_place", ""), placeholder="e.g. Algiers")
        phone       = st.text_input("Phone Number", value=ed.get("phone", ""),       placeholder="e.g. +213551234567")

        col_btn1, col_btn2 = st.columns(2)
        with col_btn1:
            submitted = st.form_submit_button(
                "💾 Save Changes" if is_edit else "➕ Add User",
                use_container_width=True
            )
        with col_btn2:
            cancelled = st.form_submit_button("✖ Cancel", use_container_width=True)

    # ── Cancel ──
    if cancelled:
        st.session_state.edit_id   = None
        st.session_state.edit_data = {}
        st.rerun()

    # ── Submit ──
    if submitted:
        data = {
            "first_name":  first_name.strip(),
            "last_name":   last_name.strip(),
            "birth_date":  birth_date.strip(),
            "birth_place": birth_place.strip(),
            "phone":       phone.strip(),
        }
        errors = validate_all_fields(data)

        if errors:
            for e in errors:
                st.error(f"❌ {e}")
        else:
            if is_edit:
                res = update_user(col, st.session_state.edit_id, data)
                if res["ok"]:
                    st.success("✅ User updated successfully!")
                    st.session_state.edit_id   = None
                    st.session_state.edit_data = {}
                    st.session_state.refresh  += 1
                    st.rerun()
                else:
                    st.error(f"❌ {res['error']}")
            else:
                res = add_user(col, data)
                if res["ok"]:
                    st.success(f"✅ User added! (ID: {res['id'][:8]}…)")
                    st.session_state.refresh += 1
                    st.rerun()
                else:
                    st.error(f"❌ {res['error']}")

    # ── Field guide ──
    with st.expander("📋 Field Requirements"):
        st.markdown("""
| Field | Rule |
|---|---|
| First / Last Name | Letters only, min 2 chars |
| Birth Date | DD/MM/YYYY, past date |
| Birth Place | Any text, min 2 chars |
| Phone | 8–15 digits, unique, may start with + |
        """)


# ══════════════════════════════════════════════
# RIGHT PANEL — SEARCH + TABLE
# ══════════════════════════════════════════════
with right:

    # ── Search bar ──
    st.markdown('<div class="card-title">🔍 SEARCH USERS</div>', unsafe_allow_html=True)
    search_q = st.text_input(
        label="search",
        label_visibility="collapsed",
        placeholder="Search by name, phone, place, or date…",
        value=st.session_state.search_q,
        key="search_input"
    )
    st.session_state.search_q = search_q

    # ── Fetch data ──
    _ = st.session_state.refresh  # force re-fetch on change
    users = search_users(col, search_q) if search_q else get_all_users(col)

    st.markdown(f"<br>", unsafe_allow_html=True)
    st.markdown(f'<div class="card-title">📋 USER RECORDS &nbsp;<span style="color:#64748b;font-weight:400;text-transform:none">({len(users)} found)</span></div>', unsafe_allow_html=True)

    if not users:
        st.info("📭 No users found. Add one using the form on the left.")
    else:
        # Build display dataframe
        df = pd.DataFrame(users)
        df = df.rename(columns={
            "_id":        "ID",
            "first_name": "First Name",
            "last_name":  "Last Name",
            "birth_date": "Birth Date",
            "birth_place":"Birth Place",
            "phone":      "Phone",
        })
        display_cols = ["First Name", "Last Name", "Birth Date", "Birth Place", "Phone"]
        st.dataframe(
            df[display_cols],
            use_container_width=True,
            hide_index=True,
            height=min(35 * (len(users) + 1) + 38, 400),
        )

        st.markdown("---")
        st.markdown('<div class="card-title">⚙️ ACTIONS — SELECT A USER</div>', unsafe_allow_html=True)

        # ── User selector ──
        user_labels = {
            u["_id"]: f"{u['first_name']} {u['last_name']} · {u['phone']}"
            for u in users
        }
        selected_label = st.selectbox(
            "Select user",
            options=list(user_labels.values()),
            label_visibility="collapsed"
        )
        selected_id = next(
            (uid for uid, label in user_labels.items() if label == selected_label),
            None
        )
        selected_user = next((u for u in users if u["_id"] == selected_id), None)

        act1, act2 = st.columns(2)

        # ── Edit button ──
        with act1:
            if st.button("✏️ Edit Selected", use_container_width=True, key="btn_edit"):
                if selected_user:
                    st.session_state.edit_id   = selected_user["_id"]
                    st.session_state.edit_data = {
                        "first_name":  selected_user["first_name"],
                        "last_name":   selected_user["last_name"],
                        "birth_date":  selected_user["birth_date"],
                        "birth_place": selected_user["birth_place"],
                        "phone":       selected_user["phone"],
                    }
                    st.rerun()

        # ── Delete button ──
        with act2:
            if st.button("🗑️ Delete Selected", use_container_width=True, key="btn_delete"):
                st.session_state.confirm_del = selected_id

        # ── Delete confirmation ──
        if st.session_state.confirm_del == selected_id and selected_user:
            st.warning(
                f"⚠️ Are you sure you want to delete **{selected_user['first_name']} "
                f"{selected_user['last_name']}**? This cannot be undone."
            )
            cf1, cf2 = st.columns(2)
            with cf1:
                if st.button("✅ Yes, Delete", key="confirm_yes", use_container_width=True):
                    res = delete_user(col, selected_id)
                    if res["ok"]:
                        st.success("✅ User deleted.")
                        st.session_state.confirm_del = None
                        st.session_state.edit_id     = None
                        st.session_state.edit_data   = {}
                        st.session_state.refresh    += 1
                        st.rerun()
                    else:
                        st.error(f"❌ {res['error']}")
            with cf2:
                if st.button("✖ Cancel", key="confirm_no", use_container_width=True):
                    st.session_state.confirm_del = None
                    st.rerun()


# ──────────────────────────────────────────────
# FOOTER
# ──────────────────────────────────────────────
st.markdown("---")
st.markdown(
    "<p style='text-align:center;color:white;font-size:0.9rem;'>"
    "Advanced User Management System -  " \
    " phd student: Liamine Bekhouche , supervisor: Dr Salim Zerougui." \
    " Larbi Ben Mhidi University 2025/2026 "
    "</p>",
    unsafe_allow_html=True
)
