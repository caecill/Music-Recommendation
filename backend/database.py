from backend.connector_neo4j import Neo4jConnection

db = Neo4jConnection()

def get_all_songs():
    query = """
    MATCH (s:Song)
    RETURN
        s.track_id AS track_id,
        s.name AS name,
        s.artist AS artist,
        s.genre AS genre,
        s.year AS year
    LIMIT 50
    """

    return db.query(query)

def get_all_users():
    query = """
    MATCH (u:User)

    RETURN
        u.user_id AS user_id
    LIMIT 50
    """

    return db.query(query)

def get_user_history(user_id):
    query = """
    MATCH (u:User)-[r:LISTENED]->(s:Song)

    WHERE u.user_id = $user_id

    RETURN
        u.user_id AS user_id,
        s.track_id AS track_id,
        s.name AS song_name,
        s.artist AS artist,
        r.playcount AS playcount

    ORDER BY r.playcount DESC
    """

    return db.query(
        query,
        {"user_id": user_id}
    )

def register_user(user_id):
    query = """
    MERGE (u:User{user_id: $user_id})
    
    RETURN
        u.user_id AS user_id
    """
    
    return db.query(
        query,
        {"user_id": user_id}
    )

def login_user(user_id):
    query = """
    MATCH (u:User {user_id: $user_id})
    
    RETURN
        u.user_id AS user_id
    """
    
    return db.query(
        query,
        {"user_id": user_id}
    )
    
def play_song(user_id, track_id):
    query = """
    MATCH (u:User {user_id: $user_id})
    MATCH (s:Song {track_id: $track_id})

    MERGE (u)-[r:LISTENED]->(s)

    ON CREATE
        SET r.playcount = 1

    ON MATCH
        SET r.playcount = r.playcount + 1

    RETURN
        u.user_id AS user_id,
        s.track_id AS track_id,
        r.playcount AS playcount
    """

    return db.query(
        query,
        {
            "user_id": user_id,
            "track_id": track_id
        }
    )
    
def get_history_dataframe():
    query = """
    MATCH (u:User)-[r:LISTENED]->(s:Song)

    RETURN
        u.user_id AS user_id,
        s.track_id AS track_id,
        r.playcount AS playcount
    """

    result = db.query(query)
    return result if result is not None else []

def get_music_dataframe():
    query = """
    MATCH (s:Song)

    RETURN
        s.track_id AS track_id,
        s.name AS name,
        s.artist AS artist,
        s.genre AS genre,
        s.year AS year,
        s.spotify_preview_url AS spotify_preview_url
    """

    result = db.query(query)
    return result if result is not None else []

def search_songs(query_str):
    q = query_str.lower()
    query = """
    MATCH (s:Song)
    WHERE toLower(s.track_id) CONTAINS $q
       OR toLower(s.name) CONTAINS $q
       OR toLower(s.artist) CONTAINS $q
       OR toLower(s.genre) CONTAINS $q
       OR toString(s.year) CONTAINS $q
    RETURN
        s.track_id AS track_id,
        s.name AS name,
        s.artist AS artist,
        s.genre AS genre,
        s.year AS year
    LIMIT 50
    """
    return db.query(query, {"q": q})
