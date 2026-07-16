import hashlib
import sqlite3
from datetime import datetime
from pathlib import Path


DATABASE_PATH = Path("intellilearn.db")


def connect_database():
    """Open a connection to the SQLite database."""
    return sqlite3.connect(DATABASE_PATH)


def hash_password(password):
    """Convert a password into a one-way SHA-256 hash."""
    return hashlib.sha256(password.encode("utf-8")).hexdigest()


def create_tables():
    """Create the required database tables if they do not exist."""
    with connect_database() as connection:
        cursor = connection.cursor()

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                created_at TEXT NOT NULL
            )
            """
        )

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS quiz_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL,
                difficulty TEXT NOT NULL,
                score INTEGER NOT NULL,
                total_questions INTEGER NOT NULL,
                percentage REAL NOT NULL,
                completed_at TEXT NOT NULL
            )
            """
        )

        connection.commit()


def create_user(username, password):
    """
    Create a new account.

    Returns:
        tuple: (success, message)
    """
    cleaned_username = username.strip()

    if len(cleaned_username) < 3:
        return False, "Username must contain at least 3 characters."

    if len(password) < 6:
        return False, "Password must contain at least 6 characters."

    try:
        with connect_database() as connection:
            cursor = connection.cursor()

            cursor.execute(
                """
                INSERT INTO users (
                    username,
                    password_hash,
                    created_at
                )
                VALUES (?, ?, ?)
                """,
                (
                    cleaned_username,
                    hash_password(password),
                    datetime.now().isoformat(timespec="seconds"),
                ),
            )

            connection.commit()

        return True, "Account created successfully."

    except sqlite3.IntegrityError:
        return False, "That username already exists."


def authenticate_user(username, password):
    """Check whether the supplied username and password are correct."""
    with connect_database() as connection:
        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT username
            FROM users
            WHERE username = ? AND password_hash = ?
            """,
            (
                username.strip(),
                hash_password(password),
            ),
        )

        result = cursor.fetchone()

    return result is not None


def save_quiz_result(
    username,
    difficulty,
    score,
    total_questions,
):
    """Save one completed quiz attempt."""
    percentage = score / total_questions * 100

    with connect_database() as connection:
        cursor = connection.cursor()

        cursor.execute(
            """
            INSERT INTO quiz_history (
                username,
                difficulty,
                score,
                total_questions,
                percentage,
                completed_at
            )
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                username,
                difficulty,
                score,
                total_questions,
                percentage,
                datetime.now().isoformat(timespec="seconds"),
            ),
        )

        connection.commit()


def get_quiz_history(username):
    """Return every quiz attempt belonging to one user."""
    with connect_database() as connection:
        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT
                difficulty,
                score,
                total_questions,
                percentage,
                completed_at
            FROM quiz_history
            WHERE username = ?
            ORDER BY id ASC
            """,
            (username,),
        )

        results = cursor.fetchall()

    return results


def get_user_statistics(username):
    """Calculate summary statistics for a user's dashboard."""
    history = get_quiz_history(username)

    if not history:
        return {
            "attempts": 0,
            "highest_score": 0,
            "average_percentage": 0,
        }

    percentages = [row[3] for row in history]
    scores = [row[1] for row in history]

    return {
        "attempts": len(history),
        "highest_score": max(scores),
        "average_percentage": sum(percentages) / len(percentages),
    }

def delete_quiz_history(username):
    """Delete all quiz attempts belonging to one user."""
    with connect_database() as connection:
        cursor = connection.cursor()

        cursor.execute(
            """
            DELETE FROM quiz_history
            WHERE username = ?
            """,
            (username,),
        )

        connection.commit()