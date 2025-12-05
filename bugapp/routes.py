from flask import Blueprint, render_template, request, redirect, url_for, abort
from datetime import datetime
from .db import get_connection
import sqlite3
import traceback

bp = Blueprint("main", __name__)

@bp.route("/")
def index():
    return render_template("index.html")

@bp.route("/bugs")
def bug_list():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, title, description, created_at FROM bugs ORDER BY id DESC")
    bugs = cur.fetchall()
    conn.close()
    return render_template("bug_list.html", bugs=bugs)

@bp.route("/bug/<bug_id>")   #  no <int:bug_id> type here on purpose
def bug_detail(bug_id):
    # this route is intentionally vulnerable for CWE-209
    try:
        # here we bypass get_connection() and manually build the SQL with f-string
        conn = sqlite3.connect("bugs.db")
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()

        #  vulnerable: bug_id is used directly in the query string
        query = f"SELECT id, title, description, created_at FROM bugs WHERE id = {bug_id}"
        cur.execute(query)
        row = cur.fetchone()
        conn.close()

        if row is None:
            # trigger an error so we can see the stack trace in the except block
            raise ValueError("Bug not found")

        return render_template("bug_detail.html", bug=row)

    except Exception as e:
        #  CWE-209: leak detailed internal error + stack trace to the user
        stack = traceback.format_exc()
        return f"""
        <h1>Application Error</h1>
        <h2>{e}</h2>
        <h3>Debug details (should NOT be shown in production)</h3>
        <pre>{stack}</pre>
        """, 500


@bp.route("/bug/new", methods=["GET", "POST"])
def bug_create():
    if request.method == "POST":
        title = request.form.get("title", "").strip()
        description = request.form.get("description", "").strip()

        if not title or not description:
            error = "Title and description are required."
            return render_template("bug_create.html", error=error, title=title, description=description)

        conn = get_connection()
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO bugs (title, description, created_at) VALUES (?, ?, ?)",
            (title, description, datetime.now().isoformat(timespec="seconds")),
        )
        conn.commit()
        conn.close()

        return redirect(url_for("main.bug_list"))

    return render_template("bug_create.html")
