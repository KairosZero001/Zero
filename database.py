#saves memory, read one memory, read all memories, delete memory, automatically create itself

import sqlite3

from config import MEMORY_DB


def connect():
    return sqlite3.connect(MEMORY_DB)


def setup_database():

    conn = connect()
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS memories(

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        category TEXT NOT NULL,

        memory_key TEXT UNIQUE,

        memory_value TEXT,

        importance INTEGER DEFAULT 5,
                
        confidence INTEGER DEFAULT 1,        

        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    conn.commit()
    conn.close()


def save_memory(category, key, value, importance, confidence):

    conn = connect()
    cur = conn.cursor()

    cur.execute("""
        INSERT OR REPLACE INTO memories
        (category, memory_key, memory_value, importance, confidence)

        VALUES (?, ?, ?, ?, ?)
    """, (category, key, value, importance, confidence))

    conn.commit()
    conn.close()

def get_memory(key):

    conn = connect()
    cur = conn.cursor()

    cur.execute("""
        SELECT memory_value
        FROM memories
        WHERE memory_key=?
    """, (key,))

    row = cur.fetchone()

    conn.close()

    if row:
        return row[0]

    return None


def get_all_memories():

    conn = connect()
    cur = conn.cursor()

    cur.execute("""
        SELECT
            category,
            memory_key,
            memory_value,
            importance

        FROM memories

        ORDER BY importance DESC,
                 created_at DESC
    """)

    rows = cur.fetchall()

    conn.close()

    return rows

def delete_memory(key):

    conn = connect()
    cur = conn.cursor()

    cur.execute("""
        DELETE FROM memories
        WHERE memory_key=?
    """, (key,))

    conn.commit()
    conn.close()
    
def get_confidence(key):

    conn = sqlite3.connect("memory.db")
    cur = conn.cursor()

    cur.execute(
        "SELECT confidence FROM memories WHERE key=?",
        (key,)
    )

    row = cur.fetchone()

    conn.close()

    if row:
        return row[0]

    return 0