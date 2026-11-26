
import os
from flask import Flask, render_template, redirect, flash, request, url_for
import db
import sqlite3
import secrets
from werkzeug.security import generate_password_hash

# Reference for form handeling using flash:
# https://flask.palletsprojects.com/en/stable/patterns/flashing/

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "dev_only_change_me")
app.teardown_appcontext(db.close_db)

# Routing to the Home page
@app.route("/")
def board():
    posts = db.get_db().execute( # connect to the database
        # fetch post content, whe its creatde and the username
        "SELECT posts.content, posts.created_at, users.username "
        # join posts with user table where the ids match
        "FROM posts JOIN users ON users.id = posts.user_id "
        # sort by newest first by post id
        "ORDER BY posts.id DESC"
    ).fetchall()
    return render_template("board.html", posts=posts) # render the board.html template


# Routing for user registration 
@app.route("/register", methods=["GET","POST"]) # "/register" "GET, POST"
def register():
    if request.method == "POST": # if post is the request method
        # get "username" from the from and trim any whitespace if applicable 
        username = request.form.get("username", "").strip()
        # get "email" from the from and trim any whitespace if applicable 
        email = request.form.get("email", "").strip()
        # get "password" and store it 
        password = request.form.get("password")

        # if "username", "password", or "email" is empty:
        if not username or not email or not password:
            flash("Error: All fields must be entered") # display error message 
            return render_template("register.html") # render the template

        try:
            # try connect to the db
            conn = db.get_db() 
            conn.execute(
                # add new user into users table
                "INSERT INTO users (username, password, email, api_key)"
                "VALUES (?, ?, ?, ?)",
                # hash password securely and gen a secret api key 32-bit
                (username, generate_password_hash(password), email, secrets.token_hex(16))) 
            conn.commit() # save changes 
        except sqlite3.IntegrityError: # if there is an error, send message
            flash("Username already in use.")   
            return render_template("register.html") # render the template 

        # if successfull show message and redirect to "board"
        flash("Account Created.")
        return redirect(url_for("board"))

    return render_template("register.html")

if __name__ == "__main__":
    if not os.path.exists(db.DB_PATH):
        db.init_db()
    app.run(host="127.0.0.1", port=5000)