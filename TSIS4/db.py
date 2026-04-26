import psycopg2
from config import load_config


def connect():
    try:
        conn = psycopg2.connect(**load_config())
        return conn
    except Exception as e:
        print("Database connection error:", e)
        return None


def create_tables():
    conn = connect()
    if conn is None:
        return

    with conn.cursor() as cur:
        cur.execute("""
            CREATE TABLE IF NOT EXISTS players (
                id SERIAL PRIMARY KEY,
                username VARCHAR(50) UNIQUE NOT NULL
            );
        """)

        cur.execute("""
            CREATE TABLE IF NOT EXISTS game_sessions (
                id SERIAL PRIMARY KEY,
                player_id INTEGER REFERENCES players(id),
                score INTEGER NOT NULL,
                level_reached INTEGER NOT NULL,
                played_at TIMESTAMP DEFAULT NOW()
            );
        """)

    conn.commit()
    conn.close()


def get_or_create_player(username):
    conn = connect()
    if conn is None:
        return None

    with conn.cursor() as cur:
        cur.execute("""
            INSERT INTO players(username)
            VALUES(%s)
            ON CONFLICT(username) DO NOTHING
        """, (username,))

        cur.execute("SELECT id FROM players WHERE username = %s", (username,))
        player_id = cur.fetchone()[0]

    conn.commit()
    conn.close()
    return player_id


def save_result(username, score, level):
    conn = connect()
    if conn is None:
        return

    player_id = get_or_create_player(username)

    with conn.cursor() as cur:
        cur.execute("""
            INSERT INTO game_sessions(player_id, score, level_reached)
            VALUES(%s, %s, %s)
        """, (player_id, score, level))

    conn.commit()
    conn.close()


def get_top_scores():
    conn = connect()
    if conn is None:
        return []

    with conn.cursor() as cur:
        cur.execute("""
            SELECT p.username, g.score, g.level_reached, g.played_at
            FROM game_sessions g
            JOIN players p ON g.player_id = p.id
            ORDER BY g.score DESC
            LIMIT 10
        """)
        rows = cur.fetchall()

    conn.close()
    return rows


def get_personal_best(username):
    conn = connect()
    if conn is None:
        return 0

    with conn.cursor() as cur:
        cur.execute("""
            SELECT COALESCE(MAX(g.score), 0)
            FROM game_sessions g
            JOIN players p ON g.player_id = p.id
            WHERE p.username = %s
        """, (username,))

        best = cur.fetchone()[0]

    conn.close()
    return best