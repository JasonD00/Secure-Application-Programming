
import os
from flask import Flask, render_template
import db

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "dev_only_change_me")
app.teardown_appcontext(db.close_db)

@app.route("/")
def board():
    posts = db.get_db().execute(
        "SELECT posts.content, posts.created_at, users.username "
        "FROM posts JOIN users ON users.id = posts.user_id "
        "ORDER BY posts.id DESC"
    ).fetchall()
    return render_template("board.html", posts=posts)

if __name__ == "__main__":
    if not os.path.exists(db.DB_PATH):
        db.init_db()
    app.run(host="127.0.0.1", port=5000)