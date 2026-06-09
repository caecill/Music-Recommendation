import pandas as pd

def get_popular_songs(history_df, music_df, top_n=10):
    """
    Memberikan rekomendasi awal untuk user baru yang belum punya riwayat listening.

    Cara kerja:
    1. Hitung total playcount setiap lagu.
    2. Urutkan dari playcount tertinggi.
    3. Ambil Top-N lagu paling populer.
    4. Gabungkan dengan metadata lagu dari music_clean.csv.

    Parameter:
    history_df: DataFrame history_clean.csv
    music_df: DataFrame music_clean.csv
    top_n: jumlah lagu populer yang ingin ditampilkan

    Return:
    DataFrame berisi lagu populer
    """

    required_history_columns = ["track_id", "playcount"]
    for col in required_history_columns:
        if col not in history_df.columns:
            raise ValueError(f"Kolom '{col}' tidak ditemukan di history_clean.csv")

    if "track_id" not in music_df.columns:
        raise ValueError("Kolom 'track_id' tidak ditemukan di music_clean.csv")

    df = history_df.copy()

    # Memastikan playcount berupa angka
    df["playcount"] = pd.to_numeric(df["playcount"], errors="coerce")
    df = df.dropna(subset=["track_id", "playcount"])

    popular = (
        df.groupby("track_id")["playcount"]
        .sum()
        .reset_index()
        .rename(columns={"playcount": "total_playcount"})
        .sort_values(by="total_playcount", ascending=False)
        .head(top_n)
    )

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

    result = popular.merge(
        music_info,
        on="track_id",
        how="left"
    )

    return result