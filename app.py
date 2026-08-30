from flask import Flask, render_template, request
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3

app = Flask(__name__)


def get_database():
    connection = sqlite3.connect("portal.db")
    connection.row_factory = sqlite3.Row
    return connection


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        connection = get_database()

        user = connection.execute(
            "SELECT * FROM users WHERE username = ?",
            (username,)
        ).fetchone()

        connection.close()

        if user and check_password_hash(user["password"], password):
            return "Login successful!"

        return "Invalid username or password!"

    return render_template("login.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        password_hash = generate_password_hash(password)

        connection = get_database()

        connection.execute(
            "INSERT INTO users (username, password) VALUES (?, ?)",
            (username, password_hash)
        )

        connection.commit()
        connection.close()

        return "Registration successful!"

    return render_template("register.html")


if __name__ == "__main__":
    app.run(debug=True)