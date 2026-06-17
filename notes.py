from flask import Flask, render_template, request , redirect, session, flash
import sqlite3
import os

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "fallback-key-for-local-only")

@app.route("/")
def home():
    if "username" not in session:
        return redirect("/login")

    username = session["username"]
    search_query = request.args.get("search")
    conn = sqlite3.connect("notes.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    if search_query:
        search_term = "%" + search_query + "%"
        cursor.execute(
            "SELECT * FROM notes WHERE username=? AND (title LIKE ? OR content LIKE?)",
            (username, f"%{search_query}%" , f"%{search_query}%" ))
    else:
        cursor.execute("SELECT * FROM notes WHERE username = ?", (username,))
    all_notes = cursor.fetchall()
    total = len(all_notes)
    conn.close()
    return render_template("home.html", notes=all_notes, username=username, total=total)

def init_db():
    conn = sqlite3.connect("notes.db")
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS notes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    content TEXT NOT NULL,
    username TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)
    """)
    conn.commit()
    conn.close()

init_db()

@app.route("/add", methods=["GET", "POST"])
def add_note():
    if "username" not in session:
        return redirect("/login")

    if request.method == "POST":
        title = request.form['title']
        content = request.form['content']
        username = session["username"]

        conn = sqlite3.connect("notes.db")
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO notes (title, content, username) VALUES (?,?,?)",
            (title, content, username))
        conn.commit()
        conn.close()
        flash("Note added successfully")
        return redirect("/")
    return render_template("add_note.html")


@app.route("/delete/<int:note_id>")
def delete_note(note_id):
    if "username" not in session:
        return redirect("/login")

    username = session["username"]
    conn = sqlite3.connect("notes.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM notes WHERE id=? AND username=?", (note_id, username))
    conn.commit()
    conn.close()
    return redirect("/")

@app.route("/edit/<int:note_id>", methods=["GET", "POST"])
def edit_note(note_id):
    if "username" not in session:
        return redirect("/login")

    username = session["username"]
    conn = sqlite3.connect("notes.db")
    cursor = conn.cursor()

    if request.method == "POST":
        new_title = request.form['title']
        new_content = request.form['content']

        cursor.execute(
            "UPDATE notes SET title=?, content=? WHERE id=? AND username=?",
            (new_title, new_content, note_id, username)
        )
        conn.commit()
        conn.close()
        return redirect("/")
    cursor.execute("SELECT * FROM notes WHERE id=? AND username=?", (note_id, username))
    note = cursor.fetchone()
    conn.close()
    if note is None:
        return "This note is not yours", 403
    return render_template("edit_note.html", note=note)

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        session["username"] = username
        flash("Login Successful")
        return redirect("/")
    return render_template("login.html")

@app.route("/logout")
def logout():
    session.clear()
    flash("Logged out successfully")
    return redirect("/login")



if __name__ == "__main__":
    app.run(debug=False)
