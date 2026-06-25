# neo4j/queries.py

# Menampilkan semua lagu
GET_ALL_SONGS = """
MATCH (s:Song)
RETURN 
    s.track_id AS track_id,
    s.name AS name,
    s.artist AS artist,
    s.genre AS genre,
    s.year AS year
LIMIT 50
"""

# Menampilkan semua user
GET_ALL_USERS = """
MATCH (u:User)

RETURN
    u.user_id AS user_id
LIMIT 50
"""


# Menampilkan history lagu user tertentu
GET_USER_HISTORY = """
MATCH 
    (u:User)-[r:LISTENED]->(s:Song)

WHERE u.user_id = $user_id

RETURN
    u.user_id AS user_id,
    s.track_id AS track_id,
    s.name AS song_name,
    s.artist AS artist,
    r.playcount AS playcount
ORDER BY r.playcount DESC
"""


# Menampilkan semua relasi user dan lagu
GET_USER_SONG_RELATION = """
MATCH
    (u:User)-[r:LISTENED]->(s:Song)

RETURN
    u.user_id AS user_id,
    s.name AS song,
    s.artist AS artist,
    r.playcount AS playcount
LIMIT 100
"""


# Cari lagu berdasarkan genre
GET_SONG_BY_GENRE = """
MATCH (s:Song)

WHERE s.genre = $genre

RETURN
    s.name AS song,
    s.artist AS artist,
    s.genre AS genre
LIMIT 20
"""

