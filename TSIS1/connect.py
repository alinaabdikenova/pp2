import psycopg2
from config import load_config


def connect():
    try:
        params = load_config()
        conn = psycopg2.connect(**params)
        print("Connected to PostgreSQL")
        return conn
    except Exception as e:
        print("Connection error:", e)
        return None