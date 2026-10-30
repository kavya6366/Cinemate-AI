
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from database import get_all_movies


# Original sample catalogue. These movies are imported into the
# database once so that administrators can edit or delete them.
MOVIES = [
    {
        "title": "Inception",
        "year": 2010,
        "genre": "Sci-Fi Action Thriller",
        "description": "A skilled thief enters dreams to steal secrets and attempts to plant an idea inside a target's mind.",
        "keywords": "dreams subconscious heist mind technology",
    },
    {
        "title": "Interstellar",
        "year": 2014,
        "genre": "Sci-Fi Adventure Drama",
        "description": "Explorers travel through a wormhole in space to search for a future home for humanity.",
        "keywords": "space planets time travel survival family",
    },
    {
        "title": "The Matrix",
        "year": 1999,
        "genre": "Sci-Fi Action",
        "description": "A computer hacker discovers that reality is a simulated world controlled by machines.",
        "keywords": "simulation artificial intelligence virtual reality",
    },
    {
        "title": "Avatar",
        "year": 2009,
        "genre": "Sci-Fi Adventure",
        "description": "A human joins an alien community on a distant moon and must choose between two worlds.",
        "keywords": "aliens planet nature exploration technology",
    },
    {
        "title": "The Dark Knight",
        "year": 2008,
        "genre": "Action Crime Drama",
        "description": "A masked hero faces a dangerous criminal who creates chaos in a crime-ridden city.",
        "keywords": "superhero justice crime villain detective",
    },
    {
        "title": "Titanic",
        "year": 1997,
        "genre": "Romance Drama",
        "description": "Two young people from different backgrounds fall in love aboard a doomed ocean liner.",
        "keywords": "love historical ship tragedy relationship",
    },
    {
        "title": "The Notebook",
        "year": 2004,
        "genre": "Romance Drama",
        "description": "A couple experiences a passionate romance that faces challenges across many years.",
        "keywords": "love relationships memories emotional family",
    },
    {
        "title": "Avengers: Endgame",
        "year": 2019,
        "genre": "Action Sci-Fi Adventure",
        "description": "Superheroes reunite for a final battle to restore the universe after a devastating loss.",
        "keywords": "superheroes team universe time travel battle",
    },
    {
        "title": "Jurassic Park",
        "year": 1993,
        "genre": "Adventure Sci-Fi Thriller",
        "description": "Scientists create a wildlife park with genetically recreated dinosaurs, leading to danger.",
        "keywords": "dinosaurs science experiments survival creatures",
    },
    {
        "title": "The Shawshank Redemption",
        "year": 1994,
        "genre": "Drama Crime",
        "description": "Two prisoners form a lasting friendship while one quietly hopes for freedom.",
        "keywords": "friendship hope prison perseverance",
    },
    {
        "title": "Forrest Gump",
        "year": 1994,
        "genre": "Drama Romance",
        "description": "A kind-hearted man reflects on his extraordinary life and the people who shaped it.",
        "keywords": "life friendship love history inspiration",
    },
    {
        "title": "The Martian",
        "year": 2015,
        "genre": "Sci-Fi Adventure Drama",
        "description": "An astronaut stranded on Mars uses science and ingenuity to survive until rescue.",
        "keywords": "space science survival engineering planet",
    },
    {
        "title": "Finding Nemo",
        "year": 2003,
        "genre": "Animation Adventure Family",
        "description": "A clownfish travels across the ocean to find his missing son.",
        "keywords": "ocean family friendship journey sea creatures",
    },
    {
        "title": "Coco",
        "year": 2017,
        "genre": "Animation Family Fantasy",
        "description": "A young aspiring musician enters a colourful world of ancestors to understand his family.",
        "keywords": "music family memories culture fantasy",
    },
    {
        "title": "Shutter Island",
        "year": 2010,
        "genre": "Mystery Thriller Drama",
        "description": "A detective investigates a disappearance at a remote psychiatric institution.",
        "keywords": "mystery investigation psychological suspense",
    },
    {
        "title": "The Prestige",
        "year": 2006,
        "genre": "Mystery Drama Thriller",
        "description": "Two rival magicians become obsessed with outdoing each other through dangerous illusions.",
        "keywords": "magic rivalry secrets obsession mystery",
    },
    {
        "title": "La La Land",
        "year": 2016,
        "genre": "Romance Drama Music",
        "description": "A musician and an aspiring actress pursue their dreams while falling in love in Los Angeles.",
        "keywords": "music romance ambition dreams performance",
    },
    {
        "title": "Gladiator",
        "year": 2000,
        "genre": "Action Adventure Drama",
        "description": "A betrayed Roman general fights as a gladiator and seeks justice against an emperor.",
        "keywords": "ancient Rome revenge battle honour",
    },
    {
        "title": "Dune",
        "year": 2021,
        "genre": "Sci-Fi Adventure Drama",
        "description": "A young nobleman journeys to a desert planet caught in a struggle over a valuable resource.",
        "keywords": "desert planet politics prophecy survival",
    },
    {
        "title": "Spider-Man: Into the Spider-Verse",
        "year": 2018,
        "genre": "Animation Action Adventure",
        "description": "A teenager becomes a hero and encounters other versions of Spider-Man across dimensions.",
        "keywords": "superhero multiverse animation identity",
    },
]


def ensure_sample_movies_in_database():
    """Import sample movies once without overwriting existing records."""
    from database import get_connection, init_db

    init_db()

    with get_connection() as connection:
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS cinematch_catalogue_migrations (
                migration_name TEXT PRIMARY KEY,
                applied_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """
        )

        migration_name = "import_original_sample_movies_v1"

        already_imported = connection.execute(
            """
            SELECT 1
            FROM cinematch_catalogue_migrations
            WHERE migration_name = ?
            """,
            (migration_name,),
        ).fetchone()

        if already_imported:
            return

        for movie in MOVIES:
            existing = connection.execute(
                """
                SELECT id
                FROM movies
                WHERE title = ? COLLATE NOCASE
                """,
                (movie["title"],),
            ).fetchone()

            if existing is None:
                connection.execute(
                    """
                    INSERT INTO movies (
                        title, year, genre, description, keywords,
                        poster_path, trailer_url
                    )
                    VALUES (?, ?, ?, ?, ?, '', '')
                    """,
                    (
                        movie["title"],
                        movie["year"],
                        movie["genre"],
                        movie["description"],
                        movie["keywords"],
                    ),
                )

        connection.execute(
            """
            INSERT INTO cinematch_catalogue_migrations (migration_name)
            VALUES (?)
            """,
            (migration_name,),
        )


def get_movie_dataframe():
    """Read movies from the database, which is the single source of truth."""
    ensure_sample_movies_in_database()

    saved_movies = get_all_movies()

    if not saved_movies:
        return pd.DataFrame(
            columns=[
                "id",
                "title",
                "year",
                "genre",
                "description",
                "keywords",
                "poster_path",
                "trailer_url",
                "created_at",
            ]
        )

    return pd.DataFrame([dict(movie) for movie in saved_movies])


def _build_features(dataframe):
    return (
        dataframe["genre"].fillna("").astype(str)
        + " "
        + dataframe["description"].fillna("").astype(str)
        + " "
        + dataframe["keywords"].fillna("").astype(str)
    )


def recommend_movies(movie_title, number_of_recommendations=5):
    """Recommend similar movies using TF-IDF and cosine similarity."""
    dataframe = get_movie_dataframe()

    if dataframe.empty:
        return pd.DataFrame()

    matches = dataframe.index[
        dataframe["title"].astype(str).str.casefold()
        == str(movie_title).strip().casefold()
    ].tolist()

    if not matches:
        return pd.DataFrame()

    selected_index = matches[0]

    features_text = _build_features(dataframe)

    vectorizer = TfidfVectorizer(stop_words="english")
    features = vectorizer.fit_transform(features_text)

    similarity_matrix = cosine_similarity(features)

    scores = [
        (index, score)
        for index, score in enumerate(similarity_matrix[selected_index])
        if index != selected_index
    ]

    scores.sort(key=lambda item: item[1], reverse=True)

    results = []

    for index, score in scores[:max(0, number_of_recommendations)]:
        movie = dataframe.iloc[index].to_dict()
        movie["similarity"] = round(float(score) * 100, 2)
        results.append(movie)

    return pd.DataFrame(results)


def get_movie_titles():
    """Return titles currently present in the movie database."""
    dataframe = get_movie_dataframe()

    if dataframe.empty:
        return []

    return dataframe["title"].astype(str).tolist()
