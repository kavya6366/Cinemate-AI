
import pandas as pd
import streamlit as st

from database import get_connection


def get_registered_users():
    """Fetch safe account details without exposing password data."""
    with get_connection() as connection:
        rows = connection.execute(
            """
            SELECT id, username, created_at
            FROM users
            ORDER BY id DESC
            """
        ).fetchall()

    return [dict(row) for row in rows]


def delete_registered_user(user_id):
    """Delete a registered user by their database ID."""
    with get_connection() as connection:
        connection.execute(
            "DELETE FROM users WHERE id = ?",
            (int(user_id),),
        )


def render_user_management():
    """Display the user management section for administrators."""

    # Protect this section from non-admin users.
    if (
        not st.session_state.get("authenticated", False)
        or st.session_state.get("role") != "admin"
    ):
        st.error("Administrator access is required.")
        return

    st.markdown(
        """
        <div style="
            padding: 22px 0 12px 0;
        ">
            <p style="
                color: #e50914;
                font-size: 13px;
                font-weight: 700;
                letter-spacing: 2px;
                margin-bottom: 6px;
            ">ADMINISTRATION</p>
            <h1 style="
                font-size: 32px;
                margin: 0;
            ">User Management</h1>
            <p style="
                color: #a7a7b3;
                font-size: 16px;
                margin-top: 8px;
            ">
                View and manage CineMatch AI registered accounts.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    try:
        users = get_registered_users()
    except Exception as error:
        st.error("Unable to load registered users.")
        st.caption(f"Database details: {error}")
        return

    total_users = len(users)

    metric_col, info_col = st.columns([1, 2])

    with metric_col:
        st.metric("Total Registered Users", total_users)

    with info_col:
        st.info(
            "Account passwords and password hashes are never displayed here."
        )

    st.divider()

    st.subheader("Registered Accounts")

    if not users:
        st.info("No registered user accounts were found.")
        return

    search = st.text_input(
        "Search users",
        placeholder="Enter a username...",
        key="user_management_search",
    )

    filtered_users = [
        user
        for user in users
        if search.strip().casefold()
        in str(user.get("username") or "").casefold()
    ]

    st.caption(
        f"Showing {len(filtered_users)} of {total_users} registered users."
    )

    if filtered_users:
        display_users = pd.DataFrame(
            [
                {
                    "User ID": user["id"],
                    "Username": user.get("username", ""),
                    "Registered On": user.get("created_at") or "Not available",
                }
                for user in filtered_users
            ]
        )

        st.dataframe(
            display_users,
            use_container_width=True,
            hide_index=True,
        )
    else:
        st.warning("No users match your search.")

    st.divider()

    st.subheader("Delete a User Account")
    st.warning(
        "Deleting an account may be irreversible. Check the username and ID "
        "carefully before confirming."
    )

    if not filtered_users:
        st.info("No matching accounts are available to manage.")
        return

    user_options = {
        f'{user.get("username", "Unknown")} (ID: {user["id"]})': user["id"]
        for user in filtered_users
    }

    selected_label = st.selectbox(
        "Choose an account",
        options=list(user_options.keys()),
        key="user_management_selected",
    )

    selected_id = user_options[selected_label]

    confirm = st.checkbox(
        f"I confirm that I want to delete {selected_label}.",
        key=f"confirm_delete_user_{selected_id}",
    )

    if st.button(
        "Delete Selected Account",
        type="secondary",
        disabled=not confirm,
        key="delete_selected_user_button",
    ):
        try:
            delete_registered_user(selected_id)

            st.session_state.pop(
                f"confirm_delete_user_{selected_id}",
                None,
            )

            st.success("The selected account was deleted.")
            st.rerun()

        except Exception:
            st.error(
                "The account could not be deleted. The database may contain "
                "related records that prevent deletion. No database records "
                "were intentionally removed other than the selected account."
            )
