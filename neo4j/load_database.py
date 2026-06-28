from import_data import Neo4jConnection


db = Neo4jConnection()
db.query("""
CREATE INDEX song_track_id IF NOT EXISTS
FOR (s:Song)
ON (s.track_id)
""")

db.query("""
CREATE INDEX user_id IF NOT EXISTS
FOR (u:User)
ON (u.user_id)
""")

print("Indexes ready!")

# ==========================
# 1. CREATE SONG NODE
# ==========================

print("=== Import Songs ===")

CREATE_SONGS = """
LOAD CSV WITH HEADERS
FROM 'file:///music_clean.csv'
AS row

CALL {
    WITH row

    MERGE (s:Song {
        track_id: row.track_id
    })

    SET
        s.name = row.name,
        s.artist = row.artist,
        s.genre = row.genre,
        s.year = row.year,
        s.duration_ms = row.duration_ms,
        s.danceability = row.danceability,
        s.energy = row.energy,
        s.valence = row.valence

} IN TRANSACTIONS OF 200 ROWS
"""


db.query(CREATE_SONGS)

print("Song imported!")


# ==========================
# 2. CREATE USER + RELATION
# ==========================

print("=== Import History ===")


CREATE_HISTORY = """
LOAD CSV WITH HEADERS
FROM 'file:///history_clean.csv'
AS row

CALL {
    WITH row

    MERGE (u:User {
        user_id: row.user_id
    })

    MATCH (s:Song {
        track_id: row.track_id
    })

    MERGE (u)-[r:LISTENED]->(s)

    SET r.playcount = toInteger(row.playcount)

} IN TRANSACTIONS OF 1000 ROWS
"""


db.query(CREATE_HISTORY)

print("History imported!")


# ==========================
# 3. CHECK RESULT
# ==========================

result = db.query(
    """
    MATCH (s:Song)
    RETURN count(s) AS songs
    """
)

users = db.query(
    """
    MATCH (u:User)
    RETURN count(u) AS users
    """
)

relations = db.query(
    """
    MATCH ()-[r:LISTENED]->()
    RETURN count(r) AS relations
    """
)


print("\n=== DATABASE RESULT ===")
print(result)
print(users)
print(relations)


db.close()