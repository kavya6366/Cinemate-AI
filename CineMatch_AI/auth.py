
import hashlib
import hmac
import secrets
import streamlit as st

from database import get_connection, get_user_by_username

ITERATIONS = 600_000


def hash_password(password):
    """Securely hash a password using PBKDF2."""
    salt = secrets.token_bytes(16)

    derived_key = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        salt,
        ITERATIONS,
    )

    return (
        f"pbkdf2_sha256${ITERATIONS}$"
        f"{salt.hex()}${derived_key.hex()}"
    )


def verify_password(password, stored_hash):
    """Check a password against its stored hash."""
    try:
        algorithm, iterations, salt_hex, key_hex = (
            stored_hash.split("$")
        )

        if algorithm != "pbkdf2_sha256":
            return False

        derived_key = hashlib.pbkdf2_hmac(
            "sha256",
            password.encode("utf-8"),
            bytes.fromhex(salt_hex),
            int(iterations),
        )

        return hmac.compare_digest(
            derived_key.hex(),
            key_hex,
        )

    except (ValueError, TypeError, AttributeError):
        return False


def login_user(username, password):
    """
    Authenticate a registered user.

    Returns the user record if the credentials are correct.
    Returns None if the credentials are incorrect.
    """
    if not username or not password:
        return None

    user = get_user_by_username(username.strip())

    if not user:
        return None

    stored_hash = user["password_hash"]

    if not verify_password(password, stored_hash):
        return None

    return user


def logout_user():
    """Clear the current user's session and return home."""
    session_keys = (
        "authenticated",
        "user_id",
        "username",
        "user_email",
        "role",
    )

    for key in session_keys:
        st.session_state.pop(key, None)

    st.session_state["page"] = "Home"
