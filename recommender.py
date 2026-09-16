import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.decomposition import TruncatedSVD
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error


def load_data(movies_path: str = "data/movies.csv",
              ratings_path: str = "data/ratings.csv"):
    """Load and clean movies and ratings DataFrames.

    MovieLens ml-latest-small dataset (Harper & Konstan, 2015):
    - 9,742 movies  |  100,836 ratings  |  610 users
    - Rating scale: 0.5 – 5.0 (half-star, introduced Feb 2003)
    - Only users with at least 20 ratings are included
    - Tuples of the form <user, item, rating, timestamp>
    """
    movies = pd.read_csv(movies_path)
    ratings = pd.read_csv(ratings_path)

    movies["genres_cleaned"] = movies["genres"].str.replace("|", " ", regex=False)

    movies.dropna(subset=["title", "genres"], inplace=True)
    ratings.dropna(subset=["userId", "movieId", "rating"], inplace=True)
    movies.drop_duplicates(inplace=True)
    ratings.drop_duplicates(inplace=True)

    return movies, ratings


def build_user_item_matrix(ratings: pd.DataFrame) -> pd.DataFrame:
    """Pivot ratings into a user x movie matrix.

    Produces a sparse matrix where rows are users (610 unique)
    and columns are movies (up to 9,742). Missing cells are filled
    with 0, representing unrated movies.
    """
    matrix = ratings.pivot_table(
        index="userId", columns="movieId", values="rating"
    ).fillna(0)
    return matrix


def build_content_model(movies: pd.DataFrame):
    """TF-IDF vectorisation of pipe-separated genres + cosine similarity.

    Genres are taken directly from the MovieLens movies.csv file.
    Pipe separators are converted to spaces before vectorising so each
    genre token is treated as an independent feature.

    Returns tfidf_matrix and content_sim matrix.
    """
    tfidf = TfidfVectorizer(stop_words="english")
    tfidf_matrix = tfidf.fit_transform(movies["genres_cleaned"])
    content_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)
    return tfidf_matrix, content_sim


def get_content_recommendations(title: str,
                                movies: pd.DataFrame,
                                content_sim: np.ndarray,
                                n: int = 10) -> pd.DataFrame:
    """Return top-N content-similar movies for a given title.

    Performs a case-insensitive partial match if exact title is not found.
    Excludes the seed movie itself from the result set.
    """
    movies_lower = movies["title"].str.lower()
    title_lower = title.strip().lower()

    idx_series = movies.index[movies_lower == title_lower]

    if idx_series.empty:
        idx_series = movies.index[movies_lower.str.contains(title_lower, regex=False)]

    if idx_series.empty:
        return pd.DataFrame()

    idx = idx_series[0]
    pos = movies.index.get_loc(idx)

    sim_scores = list(enumerate(content_sim[pos]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1 : n + 1]

    movie_positions = [s[0] for s in sim_scores]
    scores = [round(s[1], 4) for s in sim_scores]

    result = movies.iloc[movie_positions][["title", "genres"]].copy()
    result["similarity_score"] = scores
    result.reset_index(drop=True, inplace=True)
    return result


def build_collab_model(user_item_matrix: pd.DataFrame, n_components: int = 20):
    """Truncated SVD collaborative filtering on the user-item matrix.

    The ml-latest-small matrix (610 users x 9,742 movies) is highly sparse
    (density ~1.7%). SVD with 20 latent components captures the dominant
    user-preference signals without overfitting.

    Returns (svd, pred_df) where pred_df contains predicted ratings for every
    user-movie pair, including those the user has not yet rated.
    """
    svd = TruncatedSVD(n_components=n_components, random_state=42)
    latent_matrix = svd.fit_transform(user_item_matrix)
    predicted_ratings = np.dot(latent_matrix, svd.components_)
    pred_df = pd.DataFrame(
        predicted_ratings,
        index=user_item_matrix.index,
        columns=user_item_matrix.columns,
    )
    return svd, pred_df


def get_collab_recommendations(user_id: int,
                               pred_df: pd.DataFrame,
                               user_item_matrix: pd.DataFrame,
                               movies: pd.DataFrame,
                               n: int = 10) -> pd.DataFrame:
    """Personalised Top-N recommendations via SVD predicted ratings.

    Already-rated movies are masked out so the model only surfaces
    movies the user has not yet seen. Predicted ratings are on the
    0.5-5.0 scale consistent with the MovieLens half-star rating system.
    """
    if user_id not in pred_df.index:
        return pd.DataFrame()

    user_preds = pred_df.loc[user_id].copy()
    already_rated = user_item_matrix.loc[user_id]
    already_rated_ids = already_rated[already_rated > 0].index

    user_preds = user_preds.drop(labels=already_rated_ids, errors="ignore")
    top_n = user_preds.nlargest(n)

    result = movies[movies["movieId"].isin(top_n.index)][["movieId", "title", "genres"]].copy()
    result["predicted_rating"] = result["movieId"].map(top_n).round(4)
    result = result.sort_values("predicted_rating", ascending=False)
    result.reset_index(drop=True, inplace=True)
    return result


def compute_rmse(ratings: pd.DataFrame,
                 user_item_matrix: pd.DataFrame,
                 n_components: int = 20,
                 test_size: float = 0.2) -> float:
    """RMSE evaluation on a 20% hold-out split of observed ratings.

    Only users and movies present in the training split are evaluated.
    The matrix is normalised to [0, 1] before SVD to prevent numerical
    overflow on the small sub-matrix, then rescaled back for RMSE
    computation on the original 0.5-5.0 rating scale.
    """
    known = ratings[["userId", "movieId", "rating"]].copy()
    train_data, test_data = train_test_split(known, test_size=test_size, random_state=42)

    train_matrix = train_data.pivot_table(
        index="userId", columns="movieId", values="rating"
    ).fillna(0).astype(np.float64)

    max_val = train_matrix.values.max()
    if max_val > 0:
        train_matrix = train_matrix / max_val

    svd = TruncatedSVD(n_components=min(n_components, min(train_matrix.shape) - 1),
                       random_state=42)
    latent = svd.fit_transform(train_matrix)
    pred = np.dot(latent, svd.components_)
    if max_val > 0:
        pred = pred * max_val
    pred_df = pd.DataFrame(pred, index=train_matrix.index, columns=train_matrix.columns)

    test_data = test_data[
        test_data["userId"].isin(pred_df.index) &
        test_data["movieId"].isin(pred_df.columns)
    ]

    if test_data.empty:
        return float("nan")

    y_true = test_data["rating"].values

    user_pos = pred_df.index.get_indexer(test_data["userId"].values)
    movie_pos = pred_df.columns.get_indexer(test_data["movieId"].values)

    valid_mask = (user_pos >= 0) & (movie_pos >= 0)
    y_pred = pred_df.values[user_pos[valid_mask], movie_pos[valid_mask]]
    y_true = y_true[valid_mask]

    if len(y_true) == 0:
        return float("nan")

    rmse = np.sqrt(mean_squared_error(y_true, y_pred))
    return round(rmse, 4)
