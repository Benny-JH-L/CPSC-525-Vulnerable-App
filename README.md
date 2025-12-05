CPSC 525 Final Project – CWE-209 Vulnerable Web Application

This project demonstrates CWE-209: Information Exposure Through an Error Message by building a deliberately vulnerable Flask web application (“BugBoard”), writing an automated exploit, and then applying secure coding fixes.

The repository contains:

A vulnerable version of the application (branch: main)

A fixed, secure version of the application (branch: fixed)

An exploit script that automatically detects leaked information

Documentation showing the before/after behavior

Project Structure
CPSC-525-Vulnerable-App/
│
├── app.py                     # Application entry point
├── init_db.py                 # Creates SQLite DB + sample bugs
├── requirements.txt           # Python dependencies
│
├── bugapp/                    # Flask package
│   ├── __init__.py
│   ├── routes.py              # Vulnerable or fixed route, depending on branch
│   ├── db.py
│   ├── templates/             # HTML templates
│   └── static/                # CSS
│
└── exploit/
    └── exploit_bugboard.py    # Automated exploit script

Installation Instructions

Follow these steps to run both the vulnerable and fixed versions on your machine.

1. Clone the repository
git clone https://github.com/<your-username>/CPSC-525-Vulnerable-App.git
cd CPSC-525-Vulnerable-App

2. Create and activate a Python virtual environment
python3 -m venv venv
source venv/bin/activate


If you ever close the terminal, reactivate:

source venv/bin/activate

3. Install dependencies
pip install -r requirements.txt

4. Initialize the database

This creates bugs.db and inserts three sample bug reports.

python3 init_db.py


You should see:

Database initialized and sample bugs inserted.

Running the application

Make sure your virtual environment is active:

source venv/bin/activate


Then start Flask:

python3 app.py


Visit the site at:

http://127.0.0.1:5000

You can:

View all bugs

Add new bugs

Open bug details

Running the Vulnerable Version (CWE-209 Demo)

To switch to the main branch:

git checkout main


Then run:

python3 app.py


The vulnerable version:

Uses unsafe SQL string interpolation

Leaks stack traces to the browser

Reveals file paths

Reveals SQL engine errors

Allows the exploit to extract sensitive information

Try visiting:

/bug/abc

/bug/1;DROP TABLE bugs;--

/bug/999999999999999999999

These produce large error pages exposing internal server details (CWE-209).

Running the Fixed (Secure) Version

Switch back to the fixed branch:

git checkout fixed


Run the app:

python3 app.py


The fixed version applies:

Input validation (/<int:bug_id>)
Parameterized SQL queries
Generic error messages only
No stack traces returned to the user
Debug mode disabled

Now the same attack URLs return:

clean 404 errors, or

generic 500 messages

No sensitive information is leaked.

Running the Exploit Script

The exploit tests three payloads:

non-numeric input

SQL injection–like input

very large integers that cause overflow

Run it with:
python3 exploit/exploit_bugboard.py

Expected behavior:
Vulnerable (main) branch

File paths extracted

SQL queries extracted

Python exception names extracted

Stack traces visible

Fixed (fixed) branch

No leaked file paths

No SQL queries

No exception messages

Only HTTP status + generic user message

The exploit script provides a clear before vs after demonstration of CWE-209.

What This Project Demonstrates
CWE-209: Information Exposure Through Error Messages

The vulnerable version shows how improper error handling can leak:

internal file paths

stack traces

SQL queries

Python exception messages

database schema information

How to build an exploit

We created an automated script that:

sends malicious payloads

collects the HTML response

extracts leaked paths, SQL, and exceptions

How to fix the vulnerability

By implementing:

input type enforcement

parameterized queries

abort(404) for missing bugs

generic error messages

disabling Flask debug mode

no leakage of stack traces

Summary

This project demonstrates the full lifecycle of a security vulnerability:

Build a vulnerable web app (CWE-209)

Exploit the vulnerability

Analyze the leaked information

Fix the vulnerability

Re-run the exploit to show the fix works

The repository provides everything needed to reproduce both the vulnerable and secure versions.
