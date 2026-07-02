import pandas as pd
import numpy as np

from recommender.recommendation import recommend_songs
from recommender.cold_start import get_popular_songs

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.database import (
    get_all_songs,
    get_all_users,
    get_user_history,
    register_user,
    login_user,
    play_song,
    get_history_dataframe,
    get_music_dataframe,
    search_songs
)
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from pydantic import BaseModel

class RegisterRequest(BaseModel):
    user_id: str
    
class PlayRequest(BaseModel):
    user_id: str
    track_id: str

@app.get("/")
def root():
    return {"message": "Backend Music Recommendation berhasil dijalankan!"}


@app.get("/songs")
def songs():
    return get_all_songs()

@app.get("/songs/search")
def search(q: str = ""):
    if not q.strip():
        return get_all_songs()
    return search_songs(q.strip())

@app.get("/users")
def users():
    return get_all_users()

@app.get("/history/{user_id}")
def history(user_id: str):
    return get_user_history(user_id)

@app.post("/register")
def register(data: RegisterRequest):
    return register_user(data.user_id)

@app.post("/login")
def login(data: RegisterRequest):
    result = login_user(data.user_id)
    
    if result:
        return {
            "status": "success",
            "user": result[0]
        }
        
    return{
        "status": "failed",
        "message": "User tidak ditemukan"
    }

@app.post("/play")
def play(data: PlayRequest):
    return play_song(
        data.user_id,
        data.track_id
    )

@app.get("/recommend/{user_id}")
def recommend(user_id: str):
    try:
        history = get_history_dataframe()
        music = get_music_dataframe()

        history_df = pd.DataFrame(history)
        music_df = pd.DataFrame(music)

        if history_df.empty:
            return {"status": "error", "message": "Tidak ada data history"}

        # Cek apakah user punya history
        user_history = history_df[
            history_df["user_id"] == user_id
        ]

        if user_history.empty:
            result = get_popular_songs(
                history_df,
                music_df,
                top_n=10
            )
        else:
            result = recommend_songs(
                user_id,
                history_df,
                music_df,
                top_n=10
            )

        if result is None or result.empty:
            return []

        return result.replace({np.nan: None}).to_dict(orient="records")

    except Exception as e:
        return {"status": "error", "message": str(e)}
