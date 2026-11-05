import sqlite3
from datetime import datetime
DB = "interview_prep.db"

def connect():
    con = sqlite3.connect(DB)
    con.row_factory = sqlite3.Row
    return con

def init_db():
    with connect() as con:
        con.execute("""CREATE TABLE IF NOT EXISTS attempts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            role TEXT NOT NULL, topic TEXT NOT NULL, question TEXT NOT NULL,
            answer TEXT NOT NULL, score REAL NOT NULL, technical REAL NOT NULL,
            communication REAL NOT NULL, created_at TEXT NOT NULL
        )""")

def save_session(role, topic, question, answer, feedback):
    with connect() as con:
        con.execute("""INSERT INTO attempts(role,topic,question,answer,score,technical,communication,created_at)
        VALUES(?,?,?,?,?,?,?,?)""", (role,topic,question,answer,feedback["score"],feedback["technical"],feedback["communication"],datetime.now().strftime("%Y-%m-%d %H:%M")))

def get_sessions():
    with connect() as con:
        return [dict(x) for x in con.execute("SELECT * FROM attempts ORDER BY id DESC").fetchall()]

def get_topic_stats():
    with connect() as con:
        return [dict(x) for x in con.execute("SELECT topic, ROUND(AVG(score),1) AS average, COUNT(*) AS attempts FROM attempts GROUP BY topic ORDER BY average").fetchall()]
