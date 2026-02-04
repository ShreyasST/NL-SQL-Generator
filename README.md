# 🧠 Natural Language → SQL Generator & Database Console

An interactive Streamlit application that converts natural language into SQL and provides a safe database console for managing SQLite databases.

This project combines:
- 🤖 LLM-powered SQL generation (T5)
- 🛠 Database Console (safe operations)
- 🔐 Admin Panel (destructive operations with login)

Designed as a learning + development tool for querying and managing databases without writing raw SQL manually.

---

## ✨ Features

### 🔍 SQL Generator
Convert plain English into SQL using a fine-tuned T5 model.

Examples:
- "show all students older than 20"
- "count total orders"
- "list products cheaper than 100"

---

### 🛠 Database Console (Safe Zone)
User-friendly table management without risk:

- View tables
- Create tables dynamically
- Insert rows
- Run SELECT queries only
- Auto-clearing forms
- Success notifications

No destructive queries allowed here.

---

### 🔐 Admin Panel (Danger Zone)
Protected operations:

- Admin login
- Delete tables permanently
- Logout

Separated intentionally to avoid accidental data loss.

---

## 🧱 System Design Principles

This app follows professional architecture rules:

- Database = single source of truth
- UI driven by session_state
- No blocking sleep() calls
- No destructive actions in user console
- State → rerun → render pattern

Benefits:
- Stable UI
- No flicker bugs
- No race conditions
- Predictable behavior

---

## 🧰 Tech Stack

- Streamlit
- SQLite
- PyTorch
- HuggingFace Transformers (T5)
- Pandas

---
## 📂 Project Structure
.
├── fullsql.py # main Streamlit app
├── user_db.sqlite # SQLite database file
├── nl_to_sql_model/ # trained model folder
├── nl_sql_merged_final6(1).csv- training SQL Query data
└── README.md


---

## ⚙️ Installation

### 1. Clone repository

git clone <your-repo-url>
cd <project-folder>

### 2. Install dependencies
pip install streamlit torch transformers pandas

### 3. Run the App
streamlit run fullsql.py

- Open browser:
http://localhost:8501

## 🚀 How to Use

### 1. Generate SQL
- Open SQL Generator
- Enter natural language query
- Click Generate SQL

### 2. Create Table

- Open Database Console
- Enter table name
- Add columns
- Click Create Table
- Form resets automatically.

### 3. Insert Row

- Select table
- Enter values
- Click Insert
- Row appears instantly.

### 4. Execute Query

- Enter generated SQL Query from Generator (eg:-SELECT * FROM students WHERE age> 18;)
- Click on Run Query to see the results.

### 5. Delete Table (Admin Only)

- Open Admin Panel
- Login using the below credentials:
  
🔑 Admin Credentials (Default)
username: admin
password: admin123

- Select table
- Confirm deletion

⚠️ Warning:
This action permanently drops the selected table and all its data.
Use only for removing test or unnecessary tables.
Deletion cannot be undone.

## 🎯Purpose

Built for:

- Learning SQL
- Experimenting with NL → SQL
- Quick prototyping
- Educational demos

Note: Not intended as production DB admin tool without security hardening.
