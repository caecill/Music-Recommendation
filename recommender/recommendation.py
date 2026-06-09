import pandas as pd
import numpy as np
from recommender.similarity import calculate_item_similarity


def get_user_history(user_id, history_df):
    """
    Mengambil riwayat lagu yang sudah pernah didengarkan oleh user tertentu.

    Parameter:
    user_id: ID user, contoh U1
    history_df: DataFrame history_clean.csv

    Return:
    DataFrame riwayat user
    """

    return history_df[history_df["user_id"] == user_id]


def recommend_songs(user_id, history_df, music_df, top_n=10):
    """
    Memberikan rekomendasi lagu untuk user lama menggunakan Item-Based Collaborative Filtering.

    Cara kerja:
    1. Ambil lagu yang sudah didengarkan user.
    2. Hitung similarity antar lagu.
    3. Cari lagu yang belum pernah didengarkan user.
    4. Hitung skor rekomendasi berdasarkan similarity dan playcount.
    5. Urutkan skor tertinggi.
    6. Gabungkan dengan metadata lagu dari music_clean.csv.

    Parameter:
    user_id: ID user
    history_df: DataFrame history_clean.csv
    music_df: DataFrame music_clean.csv
    top_n: jumlah rekomendasi yang ingin ditampilkan

    Return:
    DataFrame berisi rekomendasi lagu
    """

    required_history_columns = ["track_id", "user_id", "playcount"]
    for col in required_history_columns:
        if col not in history_df.columns:
            raise ValueError(f"Kolom '{col}' tidak ditemukan di history_clean.csv")

    if "track_id" not in music_df.columns:
        raise ValueError("Kolom 'track_id' tidak ditemukan di music_clean.csv")

    df = history_df.copy()

    # Memastikan playcount berupa angka
    df["playcount"] = pd.to_numeric(df["playcount"], errors="coerce")
    df = df.dropna(subset=["track_id", "user_id", "playcount"])

    # Normalisasi playcount
    df["playcount_norm"] = np.log1p(df["playcount"])

    # Ambil riwayat user
    user_history = get_user_history(user_id, df)

    # Jika user tidak punya riwayat, return kosong
    # Nanti user baru akan ditangani oleh cold_start.py
    if user_history.empty:
        return pd.DataFrame()

    # Hitung similarity antar lagu
    similarity_df = calculate_item_similarity(df)

    listened_tracks = user_history["track_id"].tolist()
    all_tracks = similarity_df.index.tolist()

    # Kandidat rekomendasi = lagu yang belum pernah didengarkan user
    candidate_tracks = [
        track for track in all_tracks
        if track not in listened_tracks
    ]

    scores = {}

    for candidate in candidate_tracks:
        weighted_sum = 0
        total_similarity = 0

        for _, row in user_history.iterrows():
            listened_track = row["track_id"]
            playcount = row["playcount_norm"]

            if candidate in similarity_df.index and listened_track in similarity_df.columns:
                sim = similarity_df.loc[candidate, listened_track]

                weighted_sum += sim * playcount
                total_similarity += sim

        # Hindari pembagian dengan nol
        if total_similarity > 0:
            scores[candidate] = weighted_sum / total_similarity

    # Urutkan skor rekomendasi dari tertinggi
    recommended = sorted(
        scores.items(),
        key=lambda x: x[1],
        reverse=True
    )[:top_n]

    result = pd.DataFrame(recommended, columns=["track_id", "score"])

    if result.empty:
        return result

    # Ambil metadata lagu yang penting untuk ditampilkan
    selected_music_columns = [
        "track_id",
        "name",
        "artist",
        "genre",
        "year",
        "spotify_preview_url"
    ]

    available_columns = [
        col for col in selected_music_columns
        if col in music_df.columns
    ]

    music_info = music_df[available_columns].drop_duplicates(subset=["track_id"])

    result = result.merge(
        music_info,
        on="track_id",
        how="left"
    )

    return result