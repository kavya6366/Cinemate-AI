
import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent / "cinematch.db"

# Folder for uploaded movie posters
POSTER_DIR = Path(__file__).resolve().parent / "movie_posters"
POSTER_DIR.mkdir(parents=True, exist_ok=True)


def get_connection():
    connection = sqlite3.connect(DB_PATH, timeout=10)
    connection.row_factory = sqlite3.Row
    return connection


def init_db():
    """Create tables and safely migrate existing databases."""
    with get_connection() as connection:
        connection.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL COLLATE NOCASE UNIQUE,
                email TEXT NOT NULL COLLATE NOCASE UNIQUE,
                password_hash TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        connection.execute("""
            CREATE TABLE IF NOT EXISTS movies (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL COLLATE NOCASE UNIQUE,
                year INTEGER NOT NULL,
                genre TEXT NOT NULL,
                description TEXT NOT NULL,
                keywords TEXT DEFAULT '',
                poster_path TEXT DEFAULT '',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # Safely add newer columns to an existing database.
        columns = {
            row["name"]
            for row in connection.execute(
                "PRAGMA table_info(movies)"
            ).fetchall()
        }

        if "trailer_url" not in columns:
            connection.execute("""
                ALTER TABLE movies
                ADD COLUMN trailer_url TEXT DEFAULT ''
            """)


def create_user(username, email, password_hash):
    try:
        with get_connection() as connection:
            connection.execute(
                """
                INSERT INTO users (username, email, password_hash)
                VALUES (?, ?, ?)
                """,
                (username.strip(), email.strip(), password_hash),
            )
        return True, "Account created successfully."

    except sqlite3.IntegrityError:
        return False, "That username or email is already registered."


def get_user_by_username(username):
    with get_connection() as connection:
        return connection.execute(
            "SELECT * FROM users WHERE username = ?",
            (username.strip(),),
        ).fetchone()


def get_user_by_email(email):
    with get_connection() as connection:
        return connection.execute(
            "SELECT * FROM users WHERE email = ?",
            (email.strip(),),
        ).fetchone()


def add_movie(
    title,
    year,
    genre,
    description,
    keywords="",
    poster_path="",
    trailer_url="",
):
    """Add a movie with optional poster and trailer."""
    try:
        init_db()

        with get_connection() as connection:
            connection.execute(
                """
                INSERT INTO movies (
                    title, year, genre, description,
                    keywords, poster_path, trailer_url
                )
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    title.strip(),
                    int(year),
                    genre.strip(),
                    description.strip(),
                    keywords.strip(),
                    poster_path,
                    trailer_url.strip(),
                ),
            )

        return True, f"{title.strip()} added successfully."

    except sqlite3.IntegrityError:
        return False, "A movie with that title already exists."

    except (sqlite3.Error, ValueError) as error:
        return False, f"Could not add movie: {error}"


def update_movie(
    movie_id,
    title,
    year,
    genre,
    description,
    keywords="",
    poster_path="",
    trailer_url="",
):
    """Update an existing movie without changing its ID."""
    try:
        init_db()

        with get_connection() as connection:
            existing = connection.execute(
                "SELECT id FROM movies WHERE id = ?",
                (int(movie_id),),
            ).fetchone()

            if existing is None:
                return False, "Movie not found."

            connection.execute(
                """
                UPDATE movies
                SET title = ?,
                    year = ?,
                    genre = ?,
                    description = ?,
                    keywords = ?,
                    poster_path = ?,
                    trailer_url = ?
                WHERE id = ?
                """,
                (
                    title.strip(),
                    int(year),
                    genre.strip(),
                    description.strip(),
                    keywords.strip(),
                    poster_path,
                    trailer_url.strip(),
                    int(movie_id),
                ),
            )

        return True, f"{title.strip()} updated successfully."

    except sqlite3.IntegrityError:
        return False, "Another movie already uses that title."

    except (sqlite3.Error, ValueError) as error:
        return False, f"Could not update movie: {error}"


def get_all_movies():
    """Return all movies, including poster and trailer details."""
    init_db()

    with get_connection() as connection:
        return connection.execute("""
            SELECT id, title, year, genre, description,
                   keywords, poster_path, trailer_url, created_at
            FROM movies
            ORDER BY title COLLATE NOCASE
        """).fetchall()


def delete_movie(movie_id):
    """Delete a movie and its locally stored poster, if safe."""
    with get_connection() as connection:
        movie = connection.execute(
            "SELECT poster_path FROM movies WHERE id = ?",
            (int(movie_id),),
        ).fetchone()

        if not movie:
            return False

        connection.execute(
            "DELETE FROM movies WHERE id = ?",
            (int(movie_id),),
        )

    # Delete only posters stored directly inside our poster directory.
    if movie["poster_path"]:
        try:
            poster = Path(movie["poster_path"]).resolve()

            if (
                poster.parent == POSTER_DIR.resolve()
                and poster.is_file()
            ):
                poster.unlink()
        except (OSError, ValueError):
            pass

    return True
