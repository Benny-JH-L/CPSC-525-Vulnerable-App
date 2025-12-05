from bugapp.db import get_connection

def init_db():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("DROP TABLE IF EXISTS bugs")

    cur.execute("""
        CREATE TABLE bugs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT NOT NULL,
            created_at TEXT NOT NULL
        )
    """)

    # sample data
    cur.execute(
        "INSERT INTO bugs (title, description, created_at) VALUES (?, ?, datetime('now'))",
        ("Login button sometimes unresponsive", "User reports that login button does nothing on first click.",),
    )
    cur.execute(
        "INSERT INTO bugs (title, description, created_at) VALUES (?, ?, datetime('now'))",
        ("Profile page 500 error", "Internal error occurs when opening profile page for some users.",),
    )

    conn.commit()
    conn.close()
    print("Database initialized and sample bugs inserted.")

if __name__ == "__main__":
    init_db()
