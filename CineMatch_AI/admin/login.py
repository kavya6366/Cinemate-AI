
import os
import hmac
import base64
from pathlib import Path

import streamlit as st


# ==========================================================
# CONFIGURATION
# ==========================================================

BASE_DIR = Path(__file__).resolve().parent.parent
BACKGROUND_IMAGE = BASE_DIR / "movie_posters" / "home_background.jpg"


# ==========================================================
# LOAD BACKGROUND IMAGE
# ==========================================================

def load_background():
    try:
        with open(BACKGROUND_IMAGE, "rb") as image_file:
            encoded = base64.b64encode(
                image_file.read()
            ).decode("utf-8")

            return f"data:image/jpeg;base64,{encoded}"

    except (OSError, ValueError):
        return ""


# ==========================================================
# NETFLIX-INSPIRED STYLES
# ==========================================================

def apply_styles(background_url):
    if background_url:
        background_css = (
            f'url("{background_url}")'
        )
    else:
        background_css = (
            "linear-gradient(135deg, #29151b, #09090d)"
        )

    st.markdown(
        f"""
        <style>
        /* Application background */

        [data-testid="stSidebar"] {{
            display: none;
        }}

        [data-testid="stHeader"] {{
            background: transparent;
        }}

        #MainMenu,
        footer {{
            visibility: hidden;
        }}

        .stApp {{
            background: #09090d;
            color: #ffffff;
        }}

        [data-testid="stAppViewContainer"] {{
            background: #09090d;
        }}

        .block-container {{
            max-width: 1300px;
            padding: 18px 4% 30px 4%;
        }}

        /* Brand */

        .cinematch-brand {{
            color: #ffffff;
            font-size: 30px;
            font-weight: 850;
            letter-spacing: -1px;
            margin-bottom: 20px;
        }}

        .cinematch-brand span {{
            color: #e50914;
        }}

        /* Background image behind the login interface */

        .admin-background {{
            position: relative;
            isolation: isolate;
            overflow: hidden;
            min-height: 690px;
            border: 1px solid #303039;
            border-radius: 14px;
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 30px 18px;
            box-sizing: border-box;
            background: #111116;
        }}

        .admin-background::before {{
            content: "";
            position: absolute;
            inset: -10px;
            z-index: -2;
            background-image: {background_css};
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
            filter: blur(7px);
            transform: scale(1.04);
        }}

        .admin-background::after {{
            content: "";
            position: absolute;
            inset: 0;
            z-index: -1;
            background: rgba(0, 0, 0, 0.64);
        }}

        /* Login heading */

        .admin-heading {{
            text-align: center;
            font-size: 32px;
            line-height: 1.2;
            font-weight: 850;
            color: #ffffff;
            margin-bottom: 10px;
        }}

        .admin-eyebrow {{
            text-align: center;
            color: #ff454d;
            font-size: 11px;
            font-weight: 800;
            letter-spacing: 2px;
            margin-bottom: 12px;
        }}

        .admin-description {{
            text-align: center;
            color: #c7c7d0;
            font-size: 14px;
            line-height: 1.7;
            margin-bottom: 24px;
        }}

        /* Native Streamlit form */

        div[data-testid="stForm"] {{
            background: rgba(12, 12, 16, 0.97);
            border: 1px solid rgba(255, 255, 255, 0.16);
            border-radius: 12px;
            padding: 30px !important;
            box-shadow: 0 18px 60px rgba(0, 0, 0, 0.42);
        }}

        [data-testid="stWidgetLabel"] p {{
            color: #f0f0f4 !important;
            font-size: 14px !important;
            font-weight: 650 !important;
        }}

        div[data-baseweb="input"] {{
            background: #202027 !important;
            border: 1px solid #41414b !important;
            border-radius: 6px !important;
        }}

        div[data-baseweb="input"] input {{
            color: #ffffff !important;
            -webkit-text-fill-color: #ffffff !important;
            caret-color: #ffffff !important;
        }}

        div[data-baseweb="input"]:focus-within {{
            border-color: #e50914 !important;
            box-shadow: 0 0 0 1px #e50914 !important;
        }}

        /* Sign in and navigation buttons */

        div.stFormSubmitButton > button {{
            min-height: 47px;
            border-radius: 6px;
            background: #e50914;
            color: #ffffff;
            border: 1px solid #e50914;
            font-size: 14px;
            font-weight: 750;
        }}

        div.stFormSubmitButton > button:hover {{
            background: #b80710;
            border-color: #b80710;
            color: #ffffff;
        }}

        div.stButton > button {{
            min-height: 44px;
            border-radius: 6px;
            background: #202027;
            color: #ffffff;
            border: 1px solid #454550;
            font-size: 14px;
            font-weight: 650;
        }}

        div.stButton > button:hover {{
            background: #333039;
            border-color: #e50914;
            color: #ffffff;
        }}

        /* Security message and footer */

        .admin-security {{
            text-align: center;
            color: #c3c3cc;
            font-size: 12px;
            line-height: 1.6;
            margin-top: 17px;
        }}

        .admin-footer {{
            text-align: center;
            color: #858591;
            font-size: 12px;
            padding-top: 22px;
        }}

        @media (max-width: 700px) {{
            .block-container {{
                padding-left: 1rem;
                padding-right: 1rem;
            }}

            .admin-background {{
                min-height: 650px;
                padding: 20px 10px;
            }}

            .admin-heading {{
                font-size: 27px;
            }}

            div[data-testid="stForm"] {{
                padding: 22px !important;
            }}
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )


# ==========================================================
# ADMINISTRATOR LOGIN PAGE
# ==========================================================

def render_admin_login():
    background_url = load_background()
    apply_styles(background_url)

    # Brand at the top
    st.markdown(
        """
        <div class="cinematch-brand">
            🎬 CineMatch <span>AI</span>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Centre the actual form horizontally on the background.
    # The login controls remain native Streamlit elements.
    outer_left, middle, outer_right = st.columns(
        [1.2, 1.6, 1.2],
        gap="small",
    )

    with middle:
        st.markdown(
            '<div style="height:55px;"></div>',
            unsafe_allow_html=True,
        )

        st.markdown(
            """
            <div class="admin-eyebrow">
                SECURE ADMINISTRATION
            </div>

            <div class="admin-heading">
                Administrator Login
            </div>

            <div class="admin-description">
                Sign in to manage the CineMatch AI movie catalogue,
                review platform statistics, and administer the system.
            </div>
            """,
            unsafe_allow_html=True,
        )

        with st.form(
            "admin_login_form",
            clear_on_submit=False,
        ):
            username = st.text_input(
                "Admin username",
                placeholder="Enter administrator username",
                key="admin_login_username",
            )

            password = st.text_input(
                "Admin password",
                type="password",
                placeholder="Enter administrator password",
                key="admin_login_password",
            )

            submitted = st.form_submit_button(
                "Sign In as Administrator",
                use_container_width=True,
            )

        if submitted:
            configured_username = os.getenv(
                "CINEMATCH_ADMIN_USERNAME"
            )
            configured_password = os.getenv(
                "CINEMATCH_ADMIN_PASSWORD"
            )

            if not configured_username or not configured_password:
                st.error(
                    "Administrator credentials are not configured. "
                    "Set CINEMATCH_ADMIN_USERNAME and "
                    "CINEMATCH_ADMIN_PASSWORD in your environment."
                )

            elif (
                hmac.compare_digest(
                    username,
                    configured_username,
                )
                and hmac.compare_digest(
                    password,
                    configured_password,
                )
            ):
                st.session_state["authenticated"] = True
                st.session_state["role"] = "admin"
                st.session_state["admin_username"] = username
                st.session_state["page"] = "Admin Dashboard"
                st.rerun()

            else:
                st.error(
                    "Invalid administrator username or password."
                )

        st.markdown(
            """
            <div class="admin-security">
                🔒 Restricted access for authorised administrators only.
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown(
            '<div style="height:16px;"></div>',
            unsafe_allow_html=True,
        )

        if st.button(
            "← Back to Home",
            key="admin_login_back_home",
            use_container_width=True,
        ):
            st.session_state["page"] = "Home"
            st.rerun()

        st.markdown(
            '<div style="height:55px;"></div>',
            unsafe_allow_html=True,
        )

    # Footer
    st.markdown(
        """
        <div class="admin-footer">
            CineMatch AI · Secure Administration Portal
        </div>
        """,
        unsafe_allow_html=True,
    )


# Do not call render_admin_login() here.
# Your app.py should call it through its existing page routing.
