import psycopg

DATABASE_URL = "postgresql://assistant:assistant@postgres:5432/assistant_db"

def get_connection():
    return psycopg.connect(DATABASE_URL)