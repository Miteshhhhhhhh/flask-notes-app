from flask import Flask, render_template, request , redirect
import sqlite3

app = Flask(__name__)

@app.route("/")
def home():
    search_query = request.args.get("search")
    conn = sqlite3.connect("notes.db")
    cursor = conn.cursor()

    if search_query:
        search_term = "%" + search_query + "%"
        cursor.execute(
            "SELECT * FROM notes WHERE title LIKE ? OR content LIKE?",
            (search_term , search_term))
    else:
        cursor.execute("SELECT * FROM notes")

    all_notes = cursor.fetchall()
    conn.close()
    return render_template("home.html", notes=all_notes)

def init_db():
    conn = sqlite3.connect("notes.db")
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS notes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    content TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)
    """)
    conn.commit()
    conn.close()

init_db()

@app.route("/add", methods=["GET", "POST"])
def add_note():
    if request.method == "POST":
        title = request.form['title']
        content = request.form['content']

        conn = sqlite3.connect("notes.db")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO notes (title, content) VALUES (?,?)", (title, content))
        conn.commit()
        conn.close()
        return redirect("/")
    return render_template("add_note.html")


@app.route("/delete/<int:note_id>")
def delete_note(note_id):
    conn = sqlite3.connect("notes.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM notes WHERE id=?", (note_id,))
    conn.commit()
    conn.close()
    return redirect("/")

@app.route("/edit/<int:note_id>", methods=["GET", "POST"])
def edit_note(note_id):
    conn = sqlite3.connect("notes.db")
    cursor = conn.cursor()

    if request.method == "POST":
        new_title = request.form['title']
        new_content = request.form['content']

        cursor.execute(
            "UPDATE notes SET title=?, content=? WHERE id=?",
            (new_title, new_content, note_id)
        )
        conn.commit()
        conn.close()
        return redirect("/")
    cursor.execute("SELECT * FROM notes WHERE id=?", (note_id,))
    note = cursor.fetchone()
    conn.close()
    return render_template("edit_note.html", note=note)



if __name__ == "__main__":
    app.run(debug=True)