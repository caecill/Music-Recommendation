from import_data import Neo4jConnection
from queries import (
    GET_ALL_SONGS,
    GET_USER_HISTORY,
    GET_USER_SONG_RELATION
)


db = Neo4jConnection()


# Test 1: ambil semua lagu
print("=== ALL SONGS ===")

songs = db.query(GET_ALL_SONGS)

for song in songs[:5]:
    print(song)


# Test 2: ambil history user tertentu
print("\n=== USER HISTORY ===")

history = db.query(
    GET_USER_HISTORY,
    {
        "user_id": "USER_12"
    }
)

for item in history[:5]:
    print(item)


# Test 3: cek relasi user-song
print("\n=== RELATION ===")

relations = db.query(GET_USER_SONG_RELATION)

for relation in relations[:5]:
    print(relation)


db.close()