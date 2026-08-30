from app import app, get_database
from werkzeug.security import generate_password_hash

def test_home_page():
    client = app.test_client()

    response = client.get("/")

    assert response.status_code == 200


def test_register_page():
    client = app.test_client()

    response = client.get("/register")

    assert response.status_code == 200

def test_login_page():
    client = app.test_client()

    response = client.get("/login")

    assert response.status_code == 200

def test_correct_login():
    client = app.test_client()

    connection = get_database()

    username = "test_user"
    password = "TestPassword123"

    connection.execute(
        "DELETE FROM users WHERE username = ?",
        (username,)
    )

    connection.execute(
        "INSERT INTO users (username, password) VALUES (?, ?)",
        (username, generate_password_hash(password))
    )

    connection.commit()
    connection.close()

    response = client.post(
        "/login",
        data={
            "username": username,
            "password": password
        }
    )

    assert response.status_code == 200
    assert b"Login successful!" in response.data

def test_incorrect_login():
    client = app.test_client()

    response = client.post(
        "/login",
        data={
            "username": "test_user",
            "password": "WrongPassword123"
        }
    )

    assert response.status_code == 200
    assert b"Invalid username or password!" in response.data    