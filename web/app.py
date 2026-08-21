import os
import sys
from functools import wraps

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from flask import Flask, render_template, request, redirect, url_for, session, jsonify, flash
import database as db
from config import SECRET_KEY, ADMIN_USERNAME, ADMIN_PASSWORD, BOT_USERNAME

app = Flask(__name__)
app.secret_key = SECRET_KEY

db.init_db()


def login_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if not session.get("logged_in"):
            return redirect(url_for("admin_login"))
        return f(*args, **kwargs)
    return wrapper


# ---------- MINI APP (foydalanuvchi tomoni) ----------

@app.route("/")
def index():
    return render_template("index.html", bot_username=BOT_USERNAME)


@app.route("/api/movies")
def api_movies():
    query = request.args.get("q", "").strip()
    movies = db.search_movies(query) if query else db.get_all_movies()
    return jsonify(movies)


@app.route("/api/movies/<code>")
def api_movie_detail(code):
    movie = db.get_movie_by_code(code)
    if not movie:
        return jsonify({"error": "not_found"}), 404
    return jsonify(movie)


# ---------- ADMIN PANEL ----------

@app.route("/admin/login", methods=["GET", "POST"])
def admin_login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            session["logged_in"] = True
            return redirect(url_for("admin_dashboard"))
        flash("❌ Login yoki parol noto'g'ri!")
    return render_template("admin_login.html")


@app.route("/admin/logout")
def admin_logout():
    session.clear()
    return redirect(url_for("admin_login"))


@app.route("/admin", methods=["GET"])
@login_required
def admin_dashboard():
    movies = db.get_all_movies()
    stats = db.get_stats()
    return render_template("admin_dashboard.html", movies=movies, stats=stats)


@app.route("/admin/add", methods=["POST"])
@login_required
def admin_add():
    try:
        db.add_movie(
            code=request.form["code"].strip(),
            title=request.form["title"].strip(),
            description=request.form.get("description", "").strip(),
            genre=request.form.get("genre", "").strip(),
            year=request.form.get("year") or None,
            poster_url=request.form.get("poster_url", "").strip(),
            video_file_id=request.form["video_file_id"].strip(),
        )
        flash("✅ Kino muvaffaqiyatli qo'shildi!")
    except Exception as e:
        flash(f"❌ Xatolik: {e}")
    return redirect(url_for("admin_dashboard"))


@app.route("/admin/edit/<int:movie_id>", methods=["POST"])
@login_required
def admin_edit(movie_id):
    try:
        db.update_movie(
            movie_id,
            code=request.form["code"].strip(),
            title=request.form["title"].strip(),
            description=request.form.get("description", "").strip(),
            genre=request.form.get("genre", "").strip(),
            year=request.form.get("year") or None,
            poster_url=request.form.get("poster_url", "").strip(),
            video_file_id=request.form["video_file_id"].strip(),
        )
        flash("✅ Kino yangilandi!")
    except Exception as e:
        flash(f"❌ Xatolik: {e}")
    return redirect(url_for("admin_dashboard"))


@app.route("/admin/delete/<int:movie_id>", methods=["POST"])
@login_required
def admin_delete(movie_id):
    db.delete_movie(movie_id)
    flash("🗑 Kino o'chirildi!")
    return redirect(url_for("admin_dashboard"))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
      
