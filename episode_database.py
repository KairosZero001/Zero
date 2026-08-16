import sqlite3

DB = "memory.db"

def setup_episode_database():

    conn = sqlite3.connect(DB)

    c = conn.cursor()

    c.execute("""
    CREATE TABLE IF NOT EXISTS episodes(

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        date TEXT,

        summary TEXT,

        importance INTEGER

    )
    """)

    conn.commit()

    conn.close()

def save_episode(date, summary, importance):

    conn = sqlite3.connect(DB)

    c = conn.cursor()

    c.execute(
        """
        INSERT INTO episodes
        (date, summary, importance)

        VALUES (?, ?, ?)
        """,
        (date, summary, importance)
    )

    conn.commit()

    conn.close()


def get_all_episodes():

    conn = sqlite3.connect(DB)

    c = conn.cursor()

    c.execute("""
        SELECT
        date,
        summary,
        importance
        FROM episodes
    """)

    rows = c.fetchall()

    conn.close()

    return rows

def episode_exists(summary):

    conn = sqlite3.connect(DB)

    c = conn.cursor()

    c.execute(
        """
        SELECT 1
        FROM episodes
        WHERE summary = ?
        LIMIT 1
        """,
        (summary,)
    )

    found = c.fetchone()

    conn.close()

    return found is not None

def recent_episodes(limit=10):

    conn = sqlite3.connect(DB)

    c = conn.cursor()

    c.execute(
        """
        SELECT
            date,
            summary,
            importance

        FROM episodes

        ORDER BY id DESC

        LIMIT ?
        """,
        (limit,)
    )

    rows = c.fetchall()

    conn.close()

    return rows