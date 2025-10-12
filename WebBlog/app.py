from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import os

app = Flask(__name__)
DB_FILE = "blog.db"

# Database setup 
def init_db():
    if not os.path.exists(DB_FILE):
        conn = sqlite3.connect(DB_FILE)
        c = conn.cursor()
        c.execute('''CREATE TABLE posts (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        title TEXT NOT NULL,
                        content TEXT NOT NULL
                    )''')
        conn.commit()
        conn.close()

def get_db_connection():
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn

# Routes 
@app.route('/')
def index():
    conn = get_db_connection()
    posts = conn.execute("SELECT * FROM posts ORDER BY id DESC").fetchall()
    conn.close()
    return render_template('index.html', posts=posts)

@app.route('/create', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        if not title or not content:
            return render_template('create.html', error="Please fill all fields.")

        conn = get_db_connection()
        conn.execute("INSERT INTO posts (title, content) VALUES (?, ?)", (title, content))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))

    return render_template('create.html')

@app.route('/edit/<int:id>', methods=('GET', 'POST'))
def edit(id):
    conn = get_db_connection()
    post = conn.execute("SELECT * FROM posts WHERE id = ?", (id,)).fetchone()

    if post is None:
        return "Post not found.", 404

    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        conn.execute("UPDATE posts SET title = ?, content = ? WHERE id = ?", (title, content, id))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))

    conn.close()
    return render_template('edit.html', post=post)

@app.route('/delete/<int:id>')
def delete(id):
    conn = get_db_connection()
    conn.execute("DELETE FROM posts WHERE id = ?", (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

# Main 
if __name__ == '__main__':
    init_db()
    app.run(debug=True)
