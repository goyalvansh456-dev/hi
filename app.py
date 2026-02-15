from flask import Flask, render_template, request, redirect
import sqlite3
from datetime import datetime

app = Flask(__name__)

# -----------------------------
# DATABASE SETUP
# -----------------------------
def init_db():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS complaints (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            room TEXT,
            category TEXT,
            description TEXT,
            assigned_to TEXT,
            status TEXT,
            created_at TEXT
        )
    """)

    conn.commit()
    conn.close()

init_db()

# -----------------------------
# AUTO ASSIGN LOGIC
# -----------------------------
def auto_assign(category):
    if category == "Electrical":
        return "Electrician"
    elif category == "Plumbing":
        return "Plumber"
    elif category == "WiFi":
        return "IT Support"
    elif category == "Furniture":
        return "Carpenter"
    else:
        return "Maintenance Staff"

# -----------------------------
# ROUTES
# -----------------------------

# Home Page
@app.route("/")
def home():
    return render_template("index.html")

# Handle Form Submission
@app.route("/submit", methods=["POST"])
def submit():
    name = request.form["name"]
    room = request.form["room"]
    category = request.form["category"]
    description = request.form["description"]

    assigned_to = auto_assign(category)
    created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO complaints
        (name, room, category, description, assigned_to, status, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (name, room, category, description, assigned_to, "Pending", created_at))

    conn.commit()
    conn.close()

    return redirect("/success")

# Simple Success Page
@app.route("/success")
def success():
    return """
    <h2>Complaint Submitted Successfully!</h2>
    <a href="/">Submit Another Complaint</a>
    <br><br>
    <a href="/admin">View All Complaints</a>
    """

# Admin Page (Basic View)
@app.route("/admin")
def admin():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM complaints ORDER BY id DESC")
    complaints = cursor.fetchall()

    conn.close()

    output = "<h2>All Complaints</h2><ul>"
    for c in complaints:
        output += f"<li>ID: {c[0]} | Name: {c[1]} | Room: {c[2]} | Issue: {c[3]} | Assigned To: {c[5]} | Status: {c[6]}</li>"
    output += "</ul><br><a href='/'>Back to Home</a>"

    return output


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)

