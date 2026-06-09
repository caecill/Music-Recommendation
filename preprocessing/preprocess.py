import pandas as pd
import os

# ==========================
# Load Dataset
# ==========================

print("Membaca dataset...")

music = pd.read_csv("data/Music.csv")
history = pd.read_csv("data/listening.csv")

print(f"Music: {music.shape}")
print(f"History: {history.shape}")

# ==========================
# Missing Value Handling
# ==========================

print("\nMenghapus missing value...")

music = music.dropna(subset=["track_id", "name", "artist"])

history = history.dropna(
    subset=["user_id", "track_id", "playcount"]
)

# ==========================
# Remove Duplicates
# ==========================

print("Menghapus data duplikat...")

music = music.drop_duplicates()

history = history.drop_duplicates()

# ==========================
# Create Mapping Track
# ==========================

print("Membuat mapping track_id...")

unique_tracks = music["track_id"].unique()

track_mapping = pd.DataFrame({
    "original_track_id": unique_tracks,
    "track_id": [f"SONG_{i+1}" for i in range(len(unique_tracks))]
})

track_map_dict = dict(
    zip(
        track_mapping["original_track_id"],
        track_mapping["track_id"]
    )
)

# ==========================
# Create Mapping User
# ==========================

print("Membuat mapping user_id...")

unique_users = history["user_id"].unique()

user_mapping = pd.DataFrame({
    "original_user_id": unique_users,
    "user_id": [f"USER_{i+1}" for i in range(len(unique_users))]
})

user_map_dict = dict(
    zip(
        user_mapping["original_user_id"],
        user_mapping["user_id"]
    )
)

# ==========================
# Apply Mapping
# ==========================

music["track_id"] = music["track_id"].map(track_map_dict)

history["track_id"] = history["track_id"].map(track_map_dict)

history["user_id"] = history["user_id"].map(user_map_dict)

# Hapus track yang tidak ditemukan
history = history.dropna(subset=["track_id"])

# ==========================
# Filter Active Users
# Minimal 3 Interaksi
# ==========================

print("Filtering user aktif...")

user_counts = history.groupby("user_id").size()

active_users = user_counts[
    user_counts >= 50
].index

history = history[
    history["user_id"].isin(active_users)
]

print(f"Jumlah user aktif: {len(active_users)}")

# ==========================
# Filter Popular Songs
# Minimal 3 Pendengar
# ==========================

print("Filtering lagu populer...")

song_counts = history.groupby("track_id").size()

popular_songs = song_counts[
    song_counts >= 50
].index

history = history[
    history["track_id"].isin(popular_songs)
]

music = music[
    music["track_id"].isin(popular_songs)
]

print(f"Jumlah lagu populer: {len(popular_songs)}")

# ==========================
# Save Output
# ==========================
os.makedirs("output", exist_ok=True)

music.to_csv(
    "output/music_clean.csv",
    index=False
)

history.to_csv(
    "output/history_clean.csv",
    index=False
)

user_mapping.to_csv(
    "output/user_mapping.csv",
    index=False
)

track_mapping.to_csv(
    "output/track_mapping.csv",
    index=False
)

print("\nSelesai!")


print(f"Music Clean: {music.shape}")
print(f"History Clean: {history.shape}")