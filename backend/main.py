import pandas as pd

from recommender.recommendation import recommend_songs
from recommender.cold_start import get_popular_songs

from fastapi import FastAPI
from backend.database import (
    get_all_songs,
    get_all_users,
    get_user_history,
    register_user,
    login_user,
    play_song,
    get_history_dataframe,
    get_music_dataframe
)
app = FastAPI()

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

    history = get_history_dataframe()
    music = get_music_dataframe()

    history_df = pd.DataFrame(history)
    music_df = pd.DataFrame(music)

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

    return result.to_dict(orient="records")