import streamlit as st
import sqlite3
import pandas as pd
import torch
from transformers import T5Tokenizer, T5ForConditionalGeneration


# =========================================================
# CONFIG
# =========================================================
ADMIN_USER = "admin"
ADMIN_PASS = "admin123"


# =========================================================
# MODEL
# =========================================================
@st.cache_resource
def load_model():
    tokenizer = T5Tokenizer.from_pretrained("nl_to_sql_model")
    model = T5ForConditionalGeneration.from_pretrained("nl_to_sql_model")
    return tokenizer, model


tokenizer, model = load_model()
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model = model.to(device)


# =========================================================
# DATABASE
# =========================================================
conn = sqlite3.connect("user_db.sqlite", check_same_thread=False)
cursor = conn.cursor()


# =========================================================
# HELPERS
# =========================================================
def get_tables():
    df = pd.read_sql_query("""
        SELECT name
        FROM sqlite_master
        WHERE type='table'
        ORDER BY name
    """, conn)
    return df["name"].tolist()


def get_columns(table):
    info = pd.read_sql_query(f'PRAGMA table_info("{table}")', conn)
    return [(row["name"], row["type"]) for _, row in info.iterrows()]


# =========================================================
# SESSION INIT
# =========================================================
defaults = {
    "page": "SQL Generator",
    "admin_logged": False,
    "clear_create_form": False,
    "table_msg": False,
    "row_msg": False,
}

for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v


# =========================================================
# SIDEBAR — BUTTON NAVIGATION (STATE SAFE)
# =========================================================
def set_page(name):
    st.session_state.page = name


st.sidebar.markdown("### 🗃️ Navigation")

st.sidebar.button("🔍 SQL Generator", on_click=set_page, args=("SQL Generator",))
st.sidebar.button("🛠️ Database Console", on_click=set_page, args=("DB Console",))
st.sidebar.button("🔐 Admin Panel", on_click=set_page, args=("Admin Panel",))

st.sidebar.caption(f"Current: {st.session_state.page}")


# =========================================================
# PAGE 1 — SQL GENERATOR
# =========================================================
if st.session_state.page == "SQL Generator":

    st.title("🧠 Natural Language → SQL Generator")

    prompt = st.text_area("Enter prompt")

    if st.button("Generate SQL"):
        if prompt.strip():
            ids = tokenizer(prompt, return_tensors="pt").input_ids.to(device)
            out = model.generate(ids, max_length=64)
            sql = tokenizer.decode(out[0], skip_special_tokens=True)
            st.code(sql, language="sql")
        else:
            st.warning("Enter a prompt first")


# =========================================================
# PAGE 2 — DATABASE CONSOLE
# =========================================================
elif st.session_state.page == "DB Console":

    st.title("🛠️ Database Console")

    # -----------------------------------------------------
    # CLEAR CREATE FORM FIRST (before widgets render)
    # -----------------------------------------------------
    if st.session_state.clear_create_form:
        st.session_state.table_name = ""

        for i in range(10):
            st.session_state[f"c{i}"] = ""
            st.session_state[f"t{i}"] = "INTEGER"

        st.session_state.clear_create_form = False

    # -----------------------------------------------------
    # SHOW MESSAGES AFTER RERUN
    # -----------------------------------------------------
    if st.session_state.table_msg:
        st.success("✅ Table created successfully")
        st.session_state.table_msg = False

    if st.session_state.row_msg:
        st.success("✅ Row inserted successfully")
        st.session_state.row_msg = False

    tables = get_tables()

    # -----------------------------------------------------
    # VIEW TABLE
    # -----------------------------------------------------
    if tables:
        selected = st.selectbox("Select table", tables)

        if selected:
            cols = get_columns(selected)

            st.subheader("Table Data")
            df = pd.read_sql_query(f'SELECT * FROM "{selected}"', conn)
            st.dataframe(df, use_container_width=True)

            # -------------------------
            # INSERT ROW
            # -------------------------
            st.subheader("Insert Row")

            with st.form("insert",clear_on_submit=True):
                values = []

                for name, dtype in cols:
                    if "DATE" in dtype.upper():
                        val = st.date_input(name)
                        values.append(val.strftime("%Y-%m-%d"))
                    else:
                        val = st.text_input(name)
                        values.append(val)

                if st.form_submit_button("Insert"):
                    q = ", ".join(["?"] * len(values))
                    cursor.execute(
                        f'INSERT INTO "{selected}" VALUES ({q})',
                        values
                    )
                    conn.commit()

                    st.session_state.row_msg = True
                    st.session_state.clear_create_form = True
                    st.rerun()

    else:
        st.info("No tables yet. Create one below.")

    # =====================================================
    # CREATE TABLE
    # =====================================================
    st.header("Create Table")

    table_name = st.text_input("Table name", key="table_name")
    n = st.number_input("Columns", 1, 10, 1)

    defs = []

    for i in range(n):
        c1, c2 = st.columns(2)
        cname = c1.text_input(f"Column {i+1}", key=f"c{i}")
        ctype = c2.selectbox("Type", ["INTEGER", "TEXT", "REAL", "DATE"], key=f"t{i}")
        defs.append((cname.strip(), ctype))

    if st.button("Create Table"):
        if table_name and all(d[0] for d in defs):

            col_str = ", ".join([f"{n} {t}" for n, t in defs])
            cursor.execute(f'CREATE TABLE "{table_name}" ({col_str})')
            conn.commit()

            st.session_state.table_msg = True
            st.rerun()

        else:
            st.error("Invalid definition")

    # =====================================================
    # SAFE QUERY
    # =====================================================
    st.header("Run SELECT Query")

    query = st.text_area("SQL (SELECT only)")

    if st.button("Run Query"):
        if query.lower().startswith("select"):
            df = pd.read_sql_query(query, conn)
            st.dataframe(df)
        else:
            st.error("Only SELECT allowed")


# =========================================================
# PAGE 3 — ADMIN PANEL
# =========================================================
elif st.session_state.page == "Admin Panel":

    st.title("🔐 Admin Panel")

    if not st.session_state.admin_logged:

        user = st.text_input("Username")
        pwd = st.text_input("Password", type="password")

        if st.button("Login"):
            if user == ADMIN_USER and pwd == ADMIN_PASS:
                st.session_state.admin_logged = True
                st.rerun()
            else:
                st.error("Invalid credentials")

    else:
        st.success("Admin authenticated")

        tables = get_tables()

        if tables:
            t = st.selectbox("Delete table", tables)
            confirm = st.checkbox("Confirm permanent deletion")

            if st.button("Delete Table") and confirm:
                cursor.execute(f'DROP TABLE "{t}"')
                conn.commit()
                st.warning(f"{t} deleted")
                st.rerun()

        if st.button("Logout"):
            st.session_state.admin_logged = False
            st.rerun()
