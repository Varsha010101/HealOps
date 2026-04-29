from flask import Flask, render_template, request, redirect, session
import json

import os

# Ensure data directory exists
os.makedirs("data", exist_ok=True)

app = Flask(__name__)
app.secret_key = "secret123"  # for session

# Ensure data directory exists
os.makedirs("data", exist_ok=True)

INCIDENT_FILE = "data/incidents.json"
USER_FILE = "data/users.json"


for file in [INCIDENT_FILE, USER_FILE]:
    if not os.path.exists(file):
        with open(file, "w") as f:
            json.dump([], f)

def load(file):
    try:
        with open(file) as f:
            return json.load(f)
    except:
        return []

def save(file, data):
    with open(file, "w") as f:
        json.dump(data, f, indent=4)

# ---------------- AUTH ----------------
@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        users = load(USER_FILE)
        username = request.form["username"]
        password = request.form["password"]

        for u in users:
            if u["username"] == username and u["password"] == password:
                session["user"] = username
                session["role"] = u["role"]
                return redirect("/dashboard")

        return "Invalid credentials"

    return render_template("login.html")
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        users = load(USER_FILE)

        new_user = {
            "username": request.form["username"],
            "password": request.form["password"],
            "role": request.form["role"]
        }

        users.append(new_user)
        save(USER_FILE, users)

        return redirect("/")

    return render_template("register.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

# ---------------- DASHBOARD ----------------

@app.route("/dashboard")
def dashboard():
    if "user" not in session:
        return redirect("/")

    incidents = load(INCIDENT_FILE)
    role = session["role"]

    return render_template("index.html", incidents=incidents, role=role, user=session["user"])

@app.route("/add", methods=["GET", "POST"])
def add():
    if "user" not in session:
        return redirect("/")

    if request.method == "POST":
        data = load(INCIDENT_FILE)

        incident = {
            "id": len(data) + 1,
            "title": request.form["title"],
            "status": "Open"
        }

        data.append(incident)
        save(INCIDENT_FILE, data)

        return redirect("/dashboard")

    return render_template("add.html")


@app.route("/resolve/<int:id>")
def resolve(id):
    if "user" not in session or session["role"] != "admin":
        return "Unauthorized", 403

    data = load(INCIDENT_FILE)

    for i in data:
        if i["id"] == id:
            i["status"] = "Resolved"

    save(INCIDENT_FILE, data)

    return redirect("/dashboard")


# ---------------- SYSTEM ----------------

@app.route("/health")
def health():
    return render_template("health.html")

import os, signal

@app.route("/crash")
def crash():
    os.kill(1, signal.SIGKILL)


# ONLY for local run (NOT Docker)
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)