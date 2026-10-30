
import uuid
import html
from pathlib import Path
from urllib.parse import urlparse
from admin.user_management import render_user_management
import pandas as pd
import streamlit as st

from database import (
    get_connection,
    get_all_movies,
    add_movie,
    update_movie,
    delete_movie,
    POSTER_DIR,
)
from services.recommender import (
    get_movie_dataframe,
    ensure_sample_movies_in_database,
)


def apply_dashboard_styles():
    st.markdown("""
    <style>
    #MainMenu, footer {visibility:hidden;}
    [data-testid="stSidebar"] {display:none;}
    [data-testid="stHeader"] {background:transparent;}

    .stApp {
        background:radial-gradient(ellipse at 75% 5%,#351015 0%,transparent 38%),
                   linear-gradient(145deg,#0c0c10,#09090c 70%);
        color:#f5f5f7;
    }
    .block-container {max-width:1450px;padding:1rem 2.5rem 3rem;}
    .brand {color:white;font-size:29px;font-weight:900;}
    .brand span,.eyebrow {color:#ff3545;}
    .eyebrow {font-size:12px;font-weight:800;letter-spacing:3px;margin-top:25px;}
    .hero-title {color:white;font-size:clamp(30px,4vw,46px);font-weight:900;margin:8px 0 12px;}
    .hero-title span {color:#f0142b;}
    .hero-description {color:#b9bbc7;font-size:16px;line-height:1.8;max-width:780px;margin-bottom:25px;}
    [data-testid="stMetric"] {
        background:linear-gradient(145deg,#21171c,#121216);
        border:1px solid #423039;border-left:4px solid #f0142b;
        border-radius:14px;padding:22px;min-height:115px;
    }
    [data-testid="stMetricLabel"] {color:#d2ccd2!important;}
    [data-testid="stMetricValue"] {color:white!important;font-weight:850!important;}
    h1,h2,h3,h4,p,label {color:#f5f5f7;}
    [data-testid="stCaptionContainer"] {color:#aaaab8;}
    [data-testid="stWidgetLabel"] p {color:#f3edf0!important;font-weight:600!important;}
    div[data-baseweb="input"],div[data-baseweb="textarea"],div[data-baseweb="select"] {
        background:#1c1b22!important;border-color:#4a3a43!important;border-radius:8px!important;
    }
    div[data-baseweb="input"] input,div[data-baseweb="textarea"] textarea {
        color:white!important;-webkit-text-fill-color:white!important;
    }
    div[data-baseweb="select"] * {color:white!important;}
    div.stButton>button,div.stFormSubmitButton>button {
        min-height:44px;border-radius:9px;font-weight:750;color:white!important;
        background:linear-gradient(135deg,#a80719,#e50924)!important;
        border:1px solid #ed2438!important;
    }
    div.stButton>button:hover,div.stFormSubmitButton>button:hover {
        background:linear-gradient(135deg,#d20b23,#ff233a)!important;
    }
    div[data-testid="stForm"] {
        background:#151419;border:1px solid #423039;border-radius:14px;padding:24px;
    }
    div[data-testid="stVerticalBlockBorderWrapper"] {
        background:linear-gradient(145deg,#17151b,#101014);
        border-color:#393039;border-radius:14px;
    }
    hr {border-color:#39262e!important;}
    .movie-meta {color:#bcb8c3;font-size:14px;line-height:1.9;}
    .section-heading {border-left:5px solid #f0142b;padding-left:14px;margin:30px 0 8px;}
    .footer {text-align:center;color:#85818c;font-size:12px;padding-top:35px;margin-top:35px;}
    @media(max-width:800px) {
        .block-container {padding:1rem;}
        .brand {font-size:23px;}
    }
    </style>
    """, unsafe_allow_html=True)


def render_page_header(eyebrow, title, description):
    st.markdown(
        f'<div class="eyebrow">{html.escape(str(eyebrow))}</div>'
        f'<div class="hero-title">{html.escape(str(title))}</div>'
        f'<div class="hero-description">{html.escape(str(description))}</div>',
        unsafe_allow_html=True,
    )


def valid_trailer_url(value):
    value = (value or "").strip()
    parsed = urlparse(value)
    return parsed.scheme == "https" and bool(parsed.netloc)


# Uploaded movie videos are stored inside the project so their paths can be
# saved in the existing trailer_url database field without changing the DB.
UPLOAD_DIR = Path(__file__).resolve().parent.parent / "uploads"


def save_uploaded_video(video_file):
    """Save an uploaded trailer and return its absolute file path."""
    if video_file is None:
        return ""

    max_size = 200 * 1024 * 1024  # 200 MB
    data = video_file.getvalue()
    if len(data) > max_size:
        raise ValueError("Video must be 200 MB or smaller.")

    extension = Path(video_file.name).suffix.lower()
    if extension not in {".mp4", ".mov", ".webm", ".m4v"}:
        raise ValueError("Unsupported video format. Use MP4, MOV, WEBM, or M4V.")

    UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
    destination = UPLOAD_DIR / f"{uuid.uuid4().hex}{extension}"
    destination.write_bytes(data)
    return str(destination.resolve())


def is_local_video(value):
    """Return True when value points to an existing locally saved video."""
    value = str(value or "").strip()
    if not value or value.startswith(("https://", "http://")):
        return False
    try:
        path = Path(value).resolve()
        return path.is_file() and path.suffix.lower() in {".mp4", ".mov", ".webm", ".m4v"}
    except (OSError, ValueError):
        return False


def save_uploaded_poster(upload):
    """Save an uploaded poster and return its absolute path."""
    if upload is None:
        return ""

    if len(upload.getvalue()) > 5 * 1024 * 1024:
        raise ValueError("Poster must be 5 MB or smaller.")

    POSTER_DIR.mkdir(parents=True, exist_ok=True)
    extension = Path(upload.name).suffix.lower()

    if extension not in {".png", ".jpg", ".jpeg", ".webp"}:
        raise ValueError("Unsupported poster format.")

    destination = POSTER_DIR / f"{uuid.uuid4().hex}{extension}"
    destination.write_bytes(upload.getvalue())
    return str(destination.resolve())



def admin_logout():
    st.session_state["confirm_admin_logout"] = True
    st.rerun()



def render_edit_form(movie):
    """Display a prefilled form for editing one saved movie."""
    movie_id = int(movie["id"])

    st.markdown("### ✏️ Edit Movie")
    st.caption("Change the details below and save your updates.")

    with st.form(f"edit_movie_form_{movie_id}"):
        title = st.text_input(
            "Movie Title *",
            value=str(movie["title"] or ""),
            key=f"edit_title_{movie_id}",
        )

        c1, c2 = st.columns(2)

        with c1:
            year = st.number_input(
                "Release Year *",
                min_value=1888,
                max_value=2100,
                value=max(1888, min(2100, int(movie["year"] or 2024))),
                step=1,
                key=f"edit_year_{movie_id}",
            )

        genres = [
            "Action", "Adventure", "Animation", "Comedy", "Crime",
            "Drama", "Fantasy", "Horror", "Mystery", "Romance",
            "Science Fiction", "Thriller", "Documentary", "Family",
            "Other",
        ]
        current_genre = str(movie["genre"] or "Other")

        with c2:
            if current_genre not in genres:
                genres.append(current_genre)

            genre = st.selectbox(
                "Genre *",
                genres,
                index=genres.index(current_genre),
                key=f"edit_genre_{movie_id}",
            )

        description = st.text_area(
            "Movie Description *",
            value=str(movie["description"] or ""),
            height=130,
            key=f"edit_description_{movie_id}",
        )

        keywords = st.text_input(
            "Recommendation Keywords",
            value=str(movie["keywords"] or ""),
            key=f"edit_keywords_{movie_id}",
        )

        current_trailer = str(movie["trailer_url"] or "").strip()
        if is_local_video(current_trailer):
            st.caption("Current trailer is a video uploaded from your computer.")
            st.video(current_trailer)
            trailer_default = ""
        else:
            trailer_default = current_trailer

        trailer_url = st.text_input(
            "Movie Trailer URL (optional)",
            value=trailer_default,
            help="Enter an HTTPS video URL, upload a replacement video, or leave both empty to keep the current trailer.",
            key=f"edit_trailer_{movie_id}",
        )
        new_trailer_file = st.file_uploader(
            "Replace Trailer from Your Computer (optional)",
            type=["mp4", "mov", "webm", "m4v"],
            key=f"edit_trailer_file_{movie_id}",
            help="MP4, MOV, WEBM, or M4V. Maximum 200 MB.",
        )

        current_poster = str(movie["poster_path"] or "")

        if current_poster:
            if current_poster.startswith(("https://", "http://")):
                st.caption("Current poster is an image URL.")
                st.image(current_poster, width=150)
            elif Path(current_poster).is_file():
                st.caption("Current poster")
                st.image(current_poster, width=150)

        new_poster = st.file_uploader(
            "Replace Poster (optional)",
            type=["png", "jpg", "jpeg", "webp"],
            key=f"edit_poster_{movie_id}",
            help="Leave empty to keep the current poster.",
        )

        remove_poster = st.checkbox(
            "Remove current poster",
            key=f"remove_poster_{movie_id}",
        )

        save_col, cancel_col = st.columns(2)

        with save_col:
            save_clicked = st.form_submit_button(
                "💾 Save Changes",
                use_container_width=True,
            )

        with cancel_col:
            cancel_clicked = st.form_submit_button(
                "Cancel Editing",
                use_container_width=True,
            )

    if cancel_clicked:
        st.session_state.pop("editing_movie_id", None)
        st.rerun()

    if not save_clicked:
        return

    if not title.strip():
        st.error("Movie title is required.")
        return

    if not description.strip():
        st.error("Movie description is required.")
        return

    if trailer_url.strip() and not valid_trailer_url(trailer_url):
        st.error("Please enter a valid HTTPS trailer URL.")
        return

    if new_trailer_file is not None and len(new_trailer_file.getvalue()) > 200 * 1024 * 1024:
        st.error("Video must be 200 MB or smaller.")
        return

    if new_poster is not None and len(new_poster.getvalue()) > 5 * 1024 * 1024:
        st.error("Poster must be 5 MB or smaller.")
        return

    saved_new_poster = ""
    saved_new_video = ""
    poster_path = current_poster
    trailer_value = current_trailer

    try:
        if new_trailer_file is not None:
            saved_new_video = save_uploaded_video(new_trailer_file)
            trailer_value = saved_new_video
        elif trailer_url.strip():
            trailer_value = trailer_url.strip()

        if remove_poster:
            poster_path = ""
        elif new_poster is not None:
            saved_new_poster = save_uploaded_poster(new_poster)
            poster_path = saved_new_poster

        success, message = update_movie(
            movie_id=movie_id,
            title=title.strip(),
            year=int(year),
            genre=genre,
            description=description.strip(),
            keywords=keywords.strip(),
            poster_path=poster_path,
            trailer_url=trailer_value,
        )

        if success:
            if saved_new_video and is_local_video(current_trailer) and current_trailer != trailer_value:
                try:
                    old_video = Path(current_trailer).resolve()
                    if old_video.parent == UPLOAD_DIR.resolve() and old_video.is_file():
                        old_video.unlink()
                except (OSError, ValueError):
                    pass
            # Remove the previous locally saved poster only after a
            # successful database update and only if it is in our folder.
            if (
                (remove_poster or saved_new_poster)
                and current_poster
                and current_poster != poster_path
            ):
                try:
                    old_path = Path(current_poster).resolve()
                    if (
                        old_path.parent == POSTER_DIR.resolve()
                        and old_path.is_file()
                    ):
                        old_path.unlink()
                except (OSError, ValueError):
                    pass

            st.session_state.pop("editing_movie_id", None)
            st.success(message)
            st.rerun()

        else:
            if saved_new_poster:
                Path(saved_new_poster).unlink(missing_ok=True)
            if saved_new_video:
                Path(saved_new_video).unlink(missing_ok=True)
            st.error(message)

    except Exception as error:
        if saved_new_poster:
            try:
                Path(saved_new_poster).unlink(missing_ok=True)
            except OSError:
                pass
        if saved_new_video:
            try:
                Path(saved_new_video).unlink(missing_ok=True)
            except OSError:
                pass
        st.error(f"Unable to update movie: {error}")


def render_admin_dashboard():
    if (
        not st.session_state.get("authenticated", False)
        or st.session_state.get("role") != "admin"
    ):
        st.error("Please log in with your administrator account.")
        st.session_state["page"] = "Admin Login"
        st.rerun()
        return
    ensure_sample_movies_in_database()

    apply_dashboard_styles()

    brand_col, account_col = st.columns([3, 1])

    with brand_col:
        st.markdown(
            '<div class="brand">🎬 CINEMATCH <span>AI</span></div>',
            unsafe_allow_html=True,
        )
        st.caption("ADMINISTRATION STUDIO")

    with account_col:
        st.markdown(
            f"**{html.escape(str(st.session_state.get('admin_username', 'Administrator')))}**"
        )

        if st.button(
            "↪ Logout",
            key="top_admin_logout",
            use_container_width=True,
        ):
            admin_logout()

    # Ask for confirmation before logging out
    if st.session_state.get("confirm_admin_logout", False):
        st.warning("Are you sure you want to log out of your admin account?")

        confirm_col, cancel_col = st.columns(2)

        with confirm_col:
            if st.button(
                "Yes, Sign out",
                key="confirm_logout_yes",
                use_container_width=True,
            ):
                for key in (
                    "authenticated",
                    "role",
                    "username",
                    "admin_username",
                    "admin_authenticated",
                    "admin_navigation",
                    "editing_movie_id",
                    "confirm_admin_logout",
                ):
                    st.session_state.pop(key, None)

                st.session_state["page"] = "Home"
                st.rerun()

        with cancel_col:
            if st.button(
                "Cancel",
                key="confirm_logout_cancel",
                use_container_width=True,
            ):
                st.session_state.pop("confirm_admin_logout", None)
                st.rerun()
    st.divider()

    if "admin_navigation" not in st.session_state:
        st.session_state["admin_navigation"] = "Dashboard"

    nav1, nav2, nav3,nav4 = st.columns(4)

    for label, column in [
    ("Dashboard", nav1),
    ("Add Movies", nav2),
    ("Movie Library", nav3),
    ("User Management", nav4),
]:
        with column:
            selected = st.session_state["admin_navigation"] == label
            if st.button(
                ("●  " if selected else "") + label,
                key=f"nav_{label}",
                type="primary" if selected else "secondary",
                use_container_width=True,
            ):
                st.session_state["admin_navigation"] = label
                st.rerun()

    page = st.session_state["admin_navigation"]

    try:
        with get_connection() as connection:
            user_count = connection.execute(
                "SELECT COUNT(*) FROM users"
            ).fetchone()[0]

            recent_users = connection.execute("""
                SELECT username, email, created_at
                FROM users ORDER BY created_at DESC LIMIT 10
            """).fetchall()

        saved_movies = get_all_movies()
        catalogue = get_movie_dataframe()

    except Exception as error:
        st.error(f"Unable to load dashboard data: {error}")
        return

    # DASHBOARD OVERVIEW
    if page == "Dashboard":
        st.markdown("""
        <div class="eyebrow">ADMIN CONTROL CENTRE</div>
        <div class="hero-title">Your cinema. <span>Your control.</span></div>
        <div class="hero-description">
        Manage your movie collection, monitor users, add trailers,
        and improve your CineMatch AI recommendation catalogue.
        </div>
        """, unsafe_allow_html=True)

        c1, c2, c3 = st.columns(3)
        c1.metric("👥 Registered Users", f"{user_count:,}")
        c2.metric("🎬 Total Movies", f"{len(catalogue):,}")
        c3.metric("＋ Admin-Added Movies", f"{len(saved_movies):,}")

        st.markdown(
            '<div class="section-heading"><h2>Quick Actions</h2></div>',
            unsafe_allow_html=True,
        )

        action1, action2 = st.columns(2)

        with action1:
            with st.container(border=True):
                st.markdown("### 🎞️ Add to Catalogue")
                st.write("Add movie details, posters, and trailer links.")
                if st.button(
                    "＋ Add a Movie →",
                    key="dashboard_add_movie",
                    use_container_width=True,
                ):
                    st.session_state["admin_navigation"] = "Add Movies"
                    st.rerun()

        with action2:
            with st.container(border=True):
                st.markdown("### 🎬 Manage Library")
                st.write("Edit movie details or delete movies from your catalogue.")
                if st.button(
                    "▤ Open Movie Library →",
                    key="dashboard_open_library",
                    use_container_width=True,
                ):
                    st.session_state["admin_navigation"] = "Movie Library"
                    st.rerun()

        st.divider()
        st.markdown("## Recent Registrations")

        if recent_users:
            st.dataframe(
                pd.DataFrame([dict(user) for user in recent_users]),
                use_container_width=True,
                hide_index=True,
            )
        else:
            st.info("No users have registered yet.")

    # ADD MOVIES
    elif page == "Add Movies":
        render_page_header(
            "CATALOGUE MANAGEMENT",
            "Add a New Movie",
            "Add film details, poster artwork, and upload a trailer video from your computer.",
        )

        with st.container(border=True):
            st.markdown("### Movie Information")
            st.caption("Poster is optional; maximum poster size: 5 MB.")

            with st.form("add_movie_form", clear_on_submit=True):
                title = st.text_input("Movie Title *", placeholder="e.g. Inception")

                c1, c2 = st.columns(2)

                with c1:
                    year = st.number_input(
                        "Release Year *",
                        min_value=1888,
                        max_value=2100,
                        value=2024,
                        step=1,
                    )

                with c2:
                    genre = st.selectbox("Genre *", [
                        "Action", "Adventure", "Animation", "Comedy",
                        "Crime", "Drama", "Fantasy", "Horror", "Mystery",
                        "Romance", "Science Fiction", "Thriller",
                        "Documentary", "Family", "Other",
                    ])

                description = st.text_area(
                    "Movie Description *",
                    placeholder="Describe the film's story...",
                    height=130,
                )
                keywords = st.text_input(
                    "Recommendation Keywords",
                    placeholder="space, adventure, mystery, friendship",
                )
                
                trailer_url = st.text_input(
                    "Movie Trailer URL (Optional)",
                    placeholder="Paste a direct video URL if available",
                    help="Optional. You can upload a video file below instead.",
                )

                trailer_file = st.file_uploader(
                    "Upload Movie Trailer from Your Computer",
                    type=["mp4", "mov", "webm", "m4v"],
                    help="Choose MP4, MOV, WEBM, or M4V. Maximum 200 MB.",
                    key="movie_trailer_upload",
                )

                poster_file = st.file_uploader(
                    "Upload Movie Poster",
                    type=["png", "jpg", "jpeg", "webp"],
                    help="Optional. Maximum 5 MB.",
                    key="movie_poster_upload",
                )


                if poster_file is not None:
                    if len(poster_file.getvalue()) <= 5 * 1024 * 1024:
                        st.image(poster_file, caption="Poster preview", width=180)
                    else:
                        st.warning("Poster exceeds the 5 MB limit.")

                submitted = st.form_submit_button(
                    "＋ Save Movie to Catalogue",
                    use_container_width=True,
                )

        if submitted:
            if not title.strip():
                st.error("Please enter a movie title.")
            elif not description.strip():
                st.error("Please enter a movie description.")
            elif trailer_url.strip() and not valid_trailer_url(trailer_url):
                st.error("Please enter a valid HTTPS trailer URL.")
            elif (
                poster_file is not None
                and len(poster_file.getvalue()) > 5 * 1024 * 1024
            ):
                st.error("The poster must be smaller than 5 MB.")
            elif trailer_file is not None and len(trailer_file.getvalue()) > 200 * 1024 * 1024:
                st.error("Video must be 200 MB or smaller.")
            else:
                saved_poster = ""
                saved_video = ""

                try:
                    if poster_file is not None:
                        saved_poster = save_uploaded_poster(poster_file)
                    if trailer_file is not None:
                        saved_video = save_uploaded_video(trailer_file)

                    trailer_value = saved_video or trailer_url.strip()
                    success, message = add_movie(
                        title=title.strip(),
                        year=int(year),
                        genre=genre,
                        description=description.strip(),
                        keywords=keywords.strip(),
                        poster_path=saved_poster,
                        trailer_url=trailer_value,
                    )

                    if success:
                        st.success(message)
                        st.rerun()
                    else:
                        if saved_poster:
                            Path(saved_poster).unlink(missing_ok=True)
                        if saved_video:
                            Path(saved_video).unlink(missing_ok=True)
                        st.error(message)

                except Exception as error:
                    if saved_poster:
                        Path(saved_poster).unlink(missing_ok=True)
                    if saved_video:
                        Path(saved_video).unlink(missing_ok=True)
                    st.error(f"Could not save movie: {error}")

        st.info(
            "Detailed descriptions and keywords can improve TF-IDF recommendations. "
            "Uploaded trailer videos are saved in the project's uploads folder. "
            "Video uploads are limited to 200 MB."
        )

    # MOVIE LIBRARY: EDIT AND DELETE
    elif page == "Movie Library":
        render_page_header(
            "YOUR COLLECTION",
            "Movie Library",
            "Search your movies, edit their information, replace posters, "
            "update trailers, or delete movies you no longer need.",
        )

        search = st.text_input(
            "🔎 Search movies",
            placeholder="Search by movie title or genre...",
        ).strip().casefold()

        saved_movies = [dict(movie) for movie in get_all_movies()]

        if not saved_movies:
            st.info("Your library is empty. Select Add Movies to add a movie.")
        else:
            filtered_movies = [
                movie for movie in saved_movies
                if search in str(movie["title"]).casefold()
                or search in str(movie["genre"]).casefold()
            ]

            st.caption(
                f"Showing {len(filtered_movies)} of {len(saved_movies)} "
                "admin-added movies"
            )

            if not filtered_movies:
                st.warning("No movies match your search.")

            for movie in filtered_movies:
                movie_id = int(movie["id"])

                with st.container(border=True):
                    poster_col, details_col = st.columns([1, 3])

                    with poster_col:
                        poster = str(movie.get("poster_path") or "")
                        if poster.startswith(("https://", "http://")):
                            st.image(poster, use_container_width=True)
                        elif poster and Path(poster).is_file():
                            st.image(poster, use_container_width=True)
                        else:
                            st.markdown(
                                '<div style="background:#21171d;border:1px solid #49232c;'
                                'border-radius:10px;padding:40px 5px;text-align:center;'
                                'font-size:36px;">🎬</div>',
                                unsafe_allow_html=True,
                            )
                            st.caption("No poster uploaded")

                    with details_col:
                        st.markdown(f"### {html.escape(str(movie['title']))}")
                        st.markdown(
                            f'<div class="movie-meta">Release year: '
                            f'{html.escape(str(movie["year"]))}<br>Genre: '
                            f'{html.escape(str(movie["genre"]))}</div>',
                            unsafe_allow_html=True,
                        )
                        st.write(movie["description"])

                        if movie.get("keywords"):
                            st.caption(f"Keywords: {movie['keywords']}")

                        trailer = str(movie.get("trailer_url") or "").strip()
                        if is_local_video(trailer):
                            st.video(trailer)
                        elif trailer and valid_trailer_url(trailer):
                            st.markdown(f"[Open movie trailer]({html.escape(trailer)} )")
                        else:
                            st.caption("No trailer uploaded or linked.")

                    edit_col, delete_col = st.columns(2)

                    with edit_col:
                        if st.button(
                            "✏️ Edit Movie",
                            key=f"edit_button_{movie_id}",
                            use_container_width=True,
                        ):
                            st.session_state["editing_movie_id"] = movie_id
                            st.rerun()

                    with delete_col:
                        with st.popover(
                            "🗑️ Delete Movie",
                            use_container_width=True,
                        ):
                            st.warning(
                                f"Delete **{movie['title']}** permanently "
                                "from the catalogue?"
                            )
                            st.caption("This action cannot be undone.")

                            confirmed = st.checkbox(
                                "Yes, I want to delete this movie.",
                                key=f"confirm_delete_{movie_id}",
                            )

                            if st.button(
                                "Confirm Delete",
                                key=f"confirm_delete_button_{movie_id}",
                                disabled=not confirmed,
                                use_container_width=True,
                            ):
                                try:
                                    deleted = delete_movie(movie_id)

                                    if deleted:
                                        if st.session_state.get(
                                            "editing_movie_id"
                                        ) == movie_id:
                                            st.session_state.pop(
                                                "editing_movie_id", None
                                            )

                                        st.success("Movie deleted successfully.")
                                        st.rerun()
                                    else:
                                        st.error("Movie was not found.")

                                except Exception as error:
                                    st.error(f"Unable to delete movie: {error}")

                    if st.session_state.get("editing_movie_id") == movie_id:
                        st.divider()
                        render_edit_form(movie)

            st.divider()
            st.caption(
                "Only movies stored in the database are managed here. "
                "Built-in sample catalogue entries are preserved."
            )
    elif page == "User Management":
        render_user_management()
        
    st.markdown(
        '<div class="footer">✦ CineMatch AI · Administration Studio ✦</div>',
        unsafe_allow_html=True,
    )
