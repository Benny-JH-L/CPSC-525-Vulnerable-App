from flask import Blueprint, render_template, request, redirect, url_for, abort, current_app
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

@bp.route("/bug/<int:bug_id>")  # ✔ enforce integer
def bug_detail(bug_id):
    try:
        # use shared helper and parameterized query
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(
            "SELECT id, title, description, created_at FROM bugs WHERE id = ?",
            (bug_id,),
        )
        bug = cur.fetchone()
        conn.close()

        if bug is None:
            # normal 404, no stack trace to user
            abort(404)

        return render_template("bug_detail.html", bug=bug)

    except Exception:
        # log full traceback on server, not to user
        current_app.logger.exception("bug_detail failed")

        # generic error message – no file paths, no SQL, no stack trace
        return (
            "An unexpected error occurred while loading this bug. "
            "Please try again later.",
            500,
        )



@bp.route("/bug/new", methods=["GET", "POST"])
def bug_create():
    if request.method == "POST":
        title = request.form.get("title", "").strip()
        description = request.form.get("description", "").strip()

        if not title or not description:
            error = "Title and description are required."
            return render_template(
                "bug_create.html",
                error=error,
                title=title,
                description=description,
            )

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
