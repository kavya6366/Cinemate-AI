
import base64
from pathlib import Path

import streamlit as st


# ==========================================================
# CONFIGURATION
# ==========================================================

BASE_DIR = Path(__file__).resolve().parent
BACKGROUND_IMAGE = BASE_DIR / "movie_posters" / "home_background.jpg"


# ==========================================================
# BACKGROUND IMAGE
# ==========================================================

def load_background():
    try:
        with open(BACKGROUND_IMAGE, "rb") as file:
            encoded = base64.b64encode(file.read()).decode("utf-8")
            return f"data:image/jpeg;base64,{encoded}"
    except (OSError, ValueError):
        return ""


# ==========================================================
# CSS DESIGN
# ==========================================================

def load_styles(background_url):
    if background_url:
        background_css = (
            f'background-image: url("{background_url}");'
        )
    else:
        background_css = (
            "background-image: linear-gradient(135deg, #25131b, #101522);"
        )

    st.markdown(
        f"""
        <style>
        [data-testid="stSidebar"] {{
            display: none;
        }}

        [data-testid="stHeader"] {{
            background: transparent;
        }}

        #MainMenu, footer {{
            visibility: hidden;
        }}

        .stApp {{
            background: #0b0b0f;
            color: #ffffff;
        }}

        [data-testid="stAppViewContainer"] {{
            background: #0b0b0f;
        }}

        .block-container {{
            max-width: 1450px;
            padding: 1rem 3% 2rem 3%;
        }}

        /* Brand */
        .brand {{
            font-size: 29px;
            font-weight: 850;
            color: white;
            letter-spacing: -1px;
            padding: 10px 0 20px 0;
        }}

        .brand span {{
            color: #e50914;
        }}

        /* Hero banner */
        .hero {{
            position: relative;
            isolation: isolate;
            overflow: hidden;
            min-height: 490px;
            border-radius: 12px;
            border: 1px solid #303039;
            padding: 55px 5%;
            display: flex;
            flex-direction: column;
            justify-content: center;
            box-sizing: border-box;
            background: #17171c;
        }}

        .hero::before {{
            content: "";
            position: absolute;
            inset: -12px;
            z-index: -2;
            {background_css}
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
            filter: blur(5px);
            transform: scale(1.04);
        }}

        .hero::after {{
            content: "";
            position: absolute;
            inset: 0;
            z-index: -1;
            background:
                linear-gradient(
                    90deg,
                    rgba(0,0,0,0.94),
                    rgba(0,0,0,0.70) 48%,
                    rgba(0,0,0,0.22)
                ),
                linear-gradient(
                    0deg,
                    #0b0b0f 0%,
                    transparent 40%
                );
        }}

        .hero-tag {{
            color: #ff454d;
            font-size: 13px;
            font-weight: 800;
            letter-spacing: 3px;
            margin-bottom: 18px;
        }}

        .hero-title {{
            color: #ffffff;
            font-size: clamp(42px, 6vw, 76px);
            font-weight: 900;
            line-height: 1.05;
            letter-spacing: -2px;
            margin-bottom: 22px;
        }}

        .hero-description {{
            color: #e0e0e8;
            font-size: 18px;
            line-height: 1.7;
            max-width: 650px;
        }}

        .hero-note {{
            color: #c5c5cf;
            font-size: 12px;
            font-weight: 700;
            letter-spacing: 1px;
            margin-top: 16px;
        }}

        /* Sections */
        .section-title {{
            font-size: 27px;
            font-weight: 800;
            color: #ffffff;
            margin: 30px 0 5px 0;
        }}

        .section-subtitle {{
            color: #aaaab7;
            font-size: 14px;
            margin-bottom: 18px;
        }}

        /* Movie cards */
        .movie-card {{
            position: relative;
            overflow: hidden;
            height: 215px;
            border: 1px solid #34343e;
            border-radius: 10px;
            padding: 17px;
            display: flex;
            flex-direction: column;
            justify-content: flex-end;
            box-sizing: border-box;
            background: linear-gradient(145deg, #39245e, #111116 80%);
        }}

        .movie-card::before {{
            content: "";
            position: absolute;
            width: 150px;
            height: 150px;
            top: -55px;
            right: -40px;
            border-radius: 50%;
            background: rgba(255,255,255,0.09);
        }}

        .movie-card.red {{
            background: linear-gradient(145deg, #572029, #151116 80%);
        }}

        .movie-card.blue {{
            background: linear-gradient(145deg, #173b59, #101116 80%);
        }}

        .movie-card.purple {{
            background: linear-gradient(145deg, #39245e, #111116 80%);
        }}

        .movie-card.gold {{
            background: linear-gradient(145deg, #59421b, #141116 80%);
        }}

        .movie-card.teal {{
            background: linear-gradient(145deg, #15504b, #111116 80%);
        }}

        .movie-card.green {{
            background: linear-gradient(145deg, #254c2d, #111116 80%);
        }}

        .movie-symbol {{
            position: absolute;
            top: 17px;
            left: 17px;
            font-size: 35px;
        }}

        .movie-category {{
            color: #ff6970;
            font-size: 11px;
            font-weight: 800;
            letter-spacing: 1.4px;
            margin-bottom: 7px;
        }}

        .movie-name {{
            color: white;
            font-size: 19px;
            font-weight: 800;
            line-height: 1.25;
        }}

        .movie-meta {{
            color: #c0c0ca;
            font-size: 12px;
            margin-top: 7px;
        }}

        /* Genre cards */
        .genre-card {{
            text-align: center;
            background: #17171e;
            border: 1px solid #34343e;
            border-radius: 9px;
            padding: 18px 5px;
            color: #f5f5f8;
            font-size: 14px;
            font-weight: 700;
        }}

        /* Feature cards */
        .feature-card {{
            min-height: 155px;
            padding: 22px;
            border: 1px solid #30303a;
            border-radius: 10px;
            background: linear-gradient(145deg, #191920, #111116);
        }}

        .feature-icon {{
            font-size: 28px;
            margin-bottom: 12px;
        }}

        .feature-title {{
            font-size: 18px;
            font-weight: 800;
            margin-bottom: 9px;
            color: white;
        }}

        .feature-text {{
            color: #b9b9c5;
            font-size: 14px;
            line-height: 1.6;
        }}

        /* Bottom banner */
        .bottom-banner {{
            margin-top: 28px;
            padding: 30px;
            border: 1px solid #34343e;
            border-radius: 12px;
            background: linear-gradient(110deg, #291317, #17131d, #111116);
        }}

        .footer-text {{
            text-align: center;
            color: #858591;
            font-size: 13px;
            padding: 30px 0 10px 0;
        }}

        /* Buttons */
        div.stButton > button {{
            min-height: 44px;
            border-radius: 7px;
            font-size: 14px;
            font-weight: 700;
            background: #222229;
            color: white;
            border: 1px solid #454550;
        }}

        div.stButton > button:hover {{
            background: #343038;
            border-color: #e50914;
            color: white;
        }}

        div.stButton > button[kind="primary"] {{
            background: #e50914;
            color: white;
            border: 1px solid #e50914;
        }}

        div.stButton > button[kind="primary"]:hover {{
            background: #b80710;
            border-color: #b80710;
        }}

        @media (max-width: 700px) {{
            .block-container {{
                padding-left: 1rem;
                padding-right: 1rem;
            }}

            .hero {{
                min-height: 400px;
                padding: 28px 22px;
            }}

            .hero-description {{
                font-size: 16px;
            }}

            .brand {{
                font-size: 24px;
            }}
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )


# ==========================================================
# NAVIGATION
# ==========================================================

def navigate_to(page_name):
    st.session_state["page"] = page_name
    st.rerun()


# ==========================================================
# MOVIE CARD
# ==========================================================

def render_movie_card(title, category, year, symbol, theme):
    st.markdown(
        f"""
        <div class="movie-card {theme}">
            <div class="movie-symbol">{symbol}</div>
            <div class="movie-category">{category.upper()}</div>
            <div class="movie-name">{title}</div>
            <div class="movie-meta">{year} &nbsp; • &nbsp; CINEMATCH PICKS</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


# ==========================================================
# HOMEPAGE
# ==========================================================

def render_homepage():
    load_styles(load_background())

    # Brand
    st.markdown(
        """
        <div class="brand">🎬 CineMatch <span>AI</span></div>
        """,
        unsafe_allow_html=True,
    )

    # Top navigation
    nav_space, nav_login, nav_register = st.columns([5, 1.3, 1.8])

    with nav_login:
        if st.button(
            "Sign In",
            key="home_top_signin",
            use_container_width=True,
        ):
            navigate_to("User Login")

    with nav_register:
        if st.button(
            "Create Account",
            key="home_top_register",
            type="primary",
            use_container_width=True,
        ):
            navigate_to("User Registration")

    # Hero section
    st.markdown(
        """
        <div class="hero">
            <div class="hero-tag">
                YOUR PERSONAL MOVIE DISCOVERY PLATFORM
            </div>
            <div class="hero-title">
                Discover Movies<br>You’ll Love.
            </div>
            <div class="hero-description">
                Find your next favourite film with intelligent movie
                recommendations. Explore movies, discover similar titles,
                and make every movie night memorable.
            </div>
            <div class="hero-note">
                SMART RECOMMENDATIONS &nbsp; • &nbsp;
                DISCOVER NEW STORIES &nbsp; • &nbsp; MOVIE NIGHT
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    hero_button, hero_space = st.columns([1.5, 5])

    with hero_button:
        if st.button(
            "▶  Explore Movies",
            key="home_explore_movies",
            type="primary",
            use_container_width=True,
        ):
            navigate_to("User Login")

    # Trending movies
    st.markdown(
        """
        <div class="section-title">Trending on CineMatch</div>
        <div class="section-subtitle">
            Popular picks to get your next movie night started.
        </div>
        """,
        unsafe_allow_html=True,
    )

    movies = [
        ("Inception", "Sci-Fi · Thriller", "2010", "🌀", "purple"),
        ("Interstellar", "Sci-Fi · Adventure", "2014", "🚀", "blue"),
        ("The Dark Knight", "Action · Crime", "2008", "🦇", "red"),
        ("The Matrix", "Sci-Fi · Action", "1999", "💊", "teal"),
        ("Titanic", "Romance · Drama", "1997", "🚢", "gold"),
        ("Avatar", "Fantasy · Adventure", "2009", "🌌", "green"),
    ]

    for start in (0, 3):
        cols = st.columns(3, gap="medium")
        for col, movie in zip(cols, movies[start:start + 3]):
            with col:
                render_movie_card(*movie)

    # Genres
    st.markdown(
        """
        <div class="section-title">Explore by Genre</div>
        <div class="section-subtitle">
            Choose a mood. Find a story.
        </div>
        """,
        unsafe_allow_html=True,
    )

    genres = [
        ("🚀", "Sci-Fi"),
        ("💥", "Action"),
        ("❤️", "Romance"),
        ("🕵️", "Thriller"),
        ("😂", "Comedy"),
        ("🐉", "Fantasy"),
    ]

    genre_cols = st.columns(6, gap="small")

    for col, genre in zip(genre_cols, genres):
        with col:
            st.markdown(
                f"""
                <div class="genre-card">
                    <div style="font-size:25px;margin-bottom:8px;">
                        {genre[0]}
                    </div>
                    {genre[1]}
                </div>
                """,
                unsafe_allow_html=True,
            )

    # Features
    st.markdown(
        """
        <div class="section-title">A Smarter Way to Find Movies</div>
        <div class="section-subtitle">
            Discover a new way to explore your next favourite film.
        </div>
        """,
        unsafe_allow_html=True,
    )

    features = [
        (
            "🤖",
            "AI Recommendations",
            "Find similar films using content-based machine learning "
            "and TF-IDF.",
        ),
        (
            "🎞️",
            "Explore the Catalogue",
            "Discover movies, browse titles, and explore different "
            "genres.",
        ),
        (
            "✨",
            "Personalised Discovery",
            "Select a movie and explore recommendations related to "
            "its content.",
        ),
    ]

    feature_cols = st.columns(3, gap="medium")

    for col, feature in zip(feature_cols, features):
        with col:
            st.markdown(
                f"""
                <div class="feature-card">
                    <div class="feature-icon">{feature[0]}</div>
                    <div class="feature-title">{feature[1]}</div>
                    <div class="feature-text">{feature[2]}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    # Bottom call-to-action
    st.markdown(
        """
        <div class="bottom-banner">
            <div style="
                color:#ff535b;
                font-size:12px;
                font-weight:800;
                letter-spacing:2px;
                margin-bottom:10px;
            ">
                YOUR NEXT GREAT WATCH STARTS HERE
            </div>
            <div style="
                color:white;
                font-size:28px;
                font-weight:850;
                margin-bottom:10px;
            ">
                Ready to discover something new?
            </div>
            <div style="
                color:#c4c4cf;
                font-size:15px;
                line-height:1.6;
            ">
                Sign in to explore the movie catalogue and get
                intelligent movie recommendations.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Three separate actions, including the restored admin button
    action_user, action_register, action_admin = st.columns(
        [1.3, 1.6, 1.8],
        gap="medium",
    )


   

    with action_admin:
        if st.button(
            "🔐 Administrator Login",
            key="home_bottom_admin",
            use_container_width=True,
        ):
            navigate_to("Admin Login")

    # Footer
    st.markdown(
        """
        <div class="footer-text">
            🎬 CineMatch AI · Discover. Explore. Enjoy.<br><br>
            An AI-powered movie recommendation project.
        </div>
        """,
        unsafe_allow_html=True,
    )


# Do not call render_homepage() here.
# app.py should call it exactly once.
