import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from scipy.sparse import csr_matrix


def build_user_item_matrix(history_df):
    """
    Membentuk user-item matrix untuk Item-Based Collaborative Filtering.

    Baris  = track_id / lagu
    Kolom  = user_id
    Nilai  = playcount yang sudah dinormalisasi dengan log(1 + playcount)

    Parameter:
    history_df: DataFrame berisi kolom track_id, user_id, playcount

    Return:
    user_item_matrix: DataFrame matrix lagu-user
    """

    required_columns = ["track_id", "user_id", "playcount"]
    for col in required_columns:
        if col not in history_df.columns:
            raise ValueError(f"Kolom '{col}' tidak ditemukan di history_clean.csv")

    df = history_df.copy()

    # Memastikan playcount bertipe angka
    df["playcount"] = pd.to_numeric(df["playcount"], errors="coerce")
    df = df.dropna(subset=["track_id", "user_id", "playcount"])

    # Normalisasi playcount agar nilai yang terlalu besar tidak mendominasi
    df["playcount_norm"] = np.log1p(df["playcount"])

    # Bentuk matrix: baris = lagu, kolom = user
    user_item_matrix = df.pivot_table(
        index="track_id",
        columns="user_id",
        values="playcount_norm",
        fill_value=0,
        aggfunc="sum"
    )

    return user_item_matrix


def calculate_item_similarity(history_df):
    """
    Menghitung cosine similarity antar lagu berdasarkan user-item matrix.

    Parameter:
    history_df: DataFrame history_clean.csv

    Return:
    similarity_df: DataFrame similarity antar track_id
    """

    user_item_matrix = build_user_item_matrix(history_df)

    # Sparse matrix digunakan agar lebih hemat memori
    sparse_matrix = csr_matrix(user_item_matrix.values)

    # Hitung similarity antar lagu
    similarity = cosine_similarity(sparse_matrix)

    similarity_df = pd.DataFrame(
        similarity,
        index=user_item_matrix.index,
        columns=user_item_matrix.index
    )

    return similarity_df