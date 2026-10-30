
import streamlit as st

from database import init_db
from styles import apply_styles
from index import render_homepage

from user.login import render_login
from user.registration import render_registration
from user.dashboard import render_dashboard
from user.logout import render_logout

from admin.login import render_admin_login
from admin.dashboard import render_admin_dashboard
from admin.logout import render_admin_logout


# ---------------- PAGE CONFIGURATION ----------------
st.set_page_config(
    page_title="CineMatch AI",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ---------------- INITIALISE APPLICATION ----------------
init_db()
apply_styles()

# ---------------- SESSION STATE ----------------
if "page" not in st.session_state:
    st.session_state["page"] = "Home"

if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False

if "role" not in st.session_state:
    st.session_state["role"] = None


# ---------------- CURRENT PAGE ----------------
page = st.session_state["page"]

# Hide sidebar on the public-facing pages.
# Keep sidebar navigation on dashboards and other pages.
if page in ("Home", "User Login", "User Registration"):
    st.markdown(
        """
        <style>
        [data-testid="stSidebar"] {
            display: none !important;
        }

        [data-testid="collapsedControl"] {
            display: none !important;
        }

        .block-container {
            padding-top: 1.5rem;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

else:
    # ---------------- SIDEBAR NAVIGATION ----------------
    with st.sidebar:
        st.markdown(
            '<div class="brand">CineMatch<span> AI</span></div>',
            unsafe_allow_html=True,
        )

        st.caption("MOVIE DISCOVERY PLATFORM")
        st.divider()

        authenticated = st.session_state["authenticated"]
        role = st.session_state["role"]

        if authenticated:
            if role == "user":
                st.write(
                    f"Welcome, {st.session_state.get('username', 'User')}"
                )

                if st.button(
                    "User Dashboard",
                    use_container_width=True,
                ):
                    st.session_state["page"] = "User Dashboard"
                    st.rerun()

                if st.button(
                    "Recommendations",
                    use_container_width=True,
                ):
                    st.session_state["page"] = "Recommendations"
                    st.rerun()

                if st.button(
                    "User Logout",
                    use_container_width=True,
                ):
                    st.session_state["page"] = "User Logout"
                    st.rerun()

            elif role == "admin":
                st.write("Administrator")

                if st.button(
                    "Admin Dashboard",
                    use_container_width=True,
                ):
                    st.session_state["page"] = "Admin Dashboard"
                    st.rerun()

                if st.button(
                    "Admin Logout",
                    use_container_width=True,
                ):
                    st.session_state["page"] = "Admin Logout"
                    st.rerun()

        else:
            if st.button("Home", use_container_width=True):
                st.session_state["page"] = "Home"
                st.rerun()

            if st.button("User Login", use_container_width=True):
                st.session_state["page"] = "User Login"
                st.rerun()

            if st.button("Create Account", use_container_width=True):
                st.session_state["page"] = "User Registration"
                st.rerun()

            if st.button("Admin Login", use_container_width=True):
                st.session_state["page"] = "Admin Login"
                st.rerun()


# ---------------- RENDER SELECTED PAGE ----------------
page = st.session_state["page"]
authenticated = st.session_state["authenticated"]
role = st.session_state["role"]


if page == "Home":
    render_homepage()

elif page == "User Registration":
    render_registration()

elif page == "User Login":
    render_login()

elif page == "User Dashboard":
    if authenticated and role == "user":
        render_dashboard()
    else:
        st.session_state["page"] = "User Login"
        st.rerun()

elif page == "User Logout":
    if authenticated and role == "user":
        render_logout()
    else:
        st.session_state["page"] = "User Login"
        st.rerun()

elif page == "Admin Login":
    render_admin_login()

elif page == "Admin Dashboard":
    if authenticated and role == "admin":
        render_admin_dashboard()
    else:
        st.session_state["page"] = "Admin Login"
        st.rerun()

elif page == "Admin Logout":
    if authenticated and role == "admin":
        render_admin_logout()
    else:
        st.session_state["page"] = "Admin Login"
        st.rerun()

elif page == "Recommendations":
    if authenticated and role == "user":
        render_dashboard()
    else:
        st.session_state["page"] = "User Login"
        st.rerun()

else:
    st.session_state["page"] = "Home"
    st.rerun()
