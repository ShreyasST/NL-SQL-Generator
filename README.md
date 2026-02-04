# 🧠 Natural Language → SQL Generator & Database Console

An interactive Streamlit application that converts natural language into SQL and provides a safe environment to manage SQLite databases.

This project combines:

- 🤖 LLM-powered SQL generation (T5)
- 🛠 Database Console for safe table operations
- 🔐 Admin Panel for controlled destructive actions

Designed for learning, experimentation, and rapid database prototyping without manually writing SQL.

---

## ✨ Features

### 🔍 SQL Generator
Convert plain English into SQL queries using a fine-tuned T5 model.

Examples:
- "show all students older than 20"
- "count total orders"
- "list products cheaper than 100"

---

### 🛠 Database Console (Safe Zone)

User-friendly database management without risk:

- View tables
- Create tables dynamically
- Insert rows
- Execute SELECT-only queries
- Auto-clearing forms
- Success notifications

No destructive queries allowed here.

---

### 🔐 Admin Panel (Danger Zone)

Protected administrative operations:

- Admin login
- Permanent table deletion
- Logout

Separated intentionally to prevent accidental data loss.

---

## 🧱 System Design Principles

- Database = single source of truth
- UI driven by session_state
- Destructive actions isolated in Admin Panel


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
```
.
├── fullsql.py                   # main Streamlit app
├── user_db.sqlite               # SQLite database
├── nl_to_sql_model/             # trained model
├── nl_sql_merged_final6(1).csv  # training dataset
└── README.md
```
---

## ⚙️ Installation

### Clone repository
git clone <your-repo-url>
cd <project-folder>

### Install dependencies
pip install streamlit torch transformers pandas

### Run the app
streamlit run fullsql.py

Open browser:
http://localhost:8501

---

## 🚀 How to Use

### Generate SQL
- Open SQL Generator
- Enter natural language query
- Click Generate SQL

### Create Table
- Open Database Console
- Enter table name
- Define columns
- Click Create Table

### Insert Row
- Select table
- Enter values
- Click Insert

### Execute Query
Only SELECT queries allowed.

### Delete Table (Admin Only)

Default credentials:
username: admin
password: admin123

⚠️ Warning: Table deletion is permanent and cannot be undone.

---

## 🎯 Purpose

Built for:
- Learning SQL
- NL → SQL experimentation
- Rapid prototyping
- Educational demos

Not intended for production use without additional security hardening.
