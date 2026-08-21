import sqlite3
from datetime import datetime
from config import DB_PATH


def get_conn():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS movies (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            code TEXT UNIQUE NOT NULL,
            title TEXT NOT NULL,
            description TEXT,
            genre TEXT,
            year INTEGER,
            poster_url TEXT,
            video_file_id TEXT NOT NULL,
            views INTEGER DEFAULT 0,
            created_at TEXT
        )
    """)
    conn.commit()
    conn.close()


def add_movie(code, title, description, genre, year, poster_url, video_file_id):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO movies (code, title, description, genre, year, poster_url, video_file_id, views, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, 0, ?)
    """, (code, title, description, genre, year, poster_url, video_file_id, datetime.now().isoformat()))
    conn.commit()
    movie_id = cur.lastrowid
    conn.close()
    return movie_id


def update_movie(movie_id, code, title, description, genre, year, poster_url, video_file_id):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("""
        UPDATE movies
        SET code=?, title=?, description=?, genre=?, year=?, poster_url=?, video_file_id=?
        WHERE id=?
    """, (code, title, description, genre, year, poster_url, video_file_id, movie_id))
    conn.commit()
    conn.close()


def delete_movie(movie_id):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("DELETE FROM movies WHERE id=?", (movie_id,))
    conn.commit()
    conn.close()


def get_all_movies():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT * FROM movies ORDER BY id DESC")
    rows = cur.fetchall()
    conn.close()
    return [dict(r) for r in rows]


def get_movie_by_id(movie_id):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT * FROM movies WHERE id=?", (movie_id,))
    row = cur.fetchone()
    conn.close()
    return dict(row) if row else None


def get_movie_by_code(code):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT * FROM movies WHERE code=?", (code,))
    row = cur.fetchone()
    conn.close()
    return dict(row) if row else None


def search_movies(query):
    conn = get_conn()
    cur = conn.cursor()
    like = f"%{query}%"
    cur.execute("""
        SELECT * FROM movies
        WHERE title LIKE ? OR code LIKE ? OR genre LIKE ?
        ORDER BY id DESC
    """, (like, like, like))
    rows = cur.fetchall()
    conn.close()
    return [dict(r) for r in rows]


def increment_views(code):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("UPDATE movies SET views = views + 1 WHERE code=?", (code,))
    conn.commit()
    conn.close()


def get_stats():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) as total, COALESCE(SUM(views),0) as views FROM movies")
    row = cur.fetchone()
    conn.close()
    return dict(row)
