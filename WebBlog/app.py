import os
import sqlite3
from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.utils import secure_filename


app = Flask(__name__)
app.secret_key = 'supersecretkey'
DATABASE = 'blog.db'
UPLOAD_FOLDER = 'static/upload' 
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Init database
def init_db():
    with sqlite3.connect(DATABASE) as conn:
        with open('schema.sql', 'r') as f:
            conn.executescript(f.read())

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/initdb')
def initdb():
    init_db()
    return "Database initialized successfully!"

# Trang chủ 
@app.route('/')
def index():
    conn = get_db_connection()
    posts = conn.execute(
        'SELECT posts.*, users.username FROM posts JOIN users ON posts.user_id = users.id ORDER BY posts.id DESC'
    ).fetchall()
    conn.close()
    return render_template('index.html', posts=posts)

# Register
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        conn = get_db_connection()
        try:
            conn.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, password))
            conn.commit()
            flash('Registration successful! Please log in.')
            return redirect(url_for('login'))
        except sqlite3.IntegrityError:
            flash('Username already exists!')
        finally:
            conn.close()
    return render_template('register.html')

# Login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        conn = get_db_connection()
        user = conn.execute('SELECT * FROM users WHERE username=? AND password=?', (username, password)).fetchone()
        conn.close()
        if user:
            session['user_id'] = user['id']
            session['username'] = user['username']
            return redirect(url_for('index'))
        flash('Invalid credentials')
    return render_template('login.html')

# Logout
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

# Create
@app.route('/create', methods=['GET', 'POST'])
def create_post():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        image = None
        if 'image' in request.files:
            file = request.files['image']
            if file.filename:
                filename = secure_filename(file.filename)
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(filepath)
                image = filename
        conn = get_db_connection()
        conn.execute(
            'INSERT INTO posts (title, content, image, user_id) VALUES (?, ?, ?, ?)',
            (title, content, image, session['user_id'])
        )
        conn.commit()
        conn.close()
        flash('Post created successfully!')
        return redirect(url_for('index'))
    return render_template('create.html')

# Xem chi tiết bài viết + bình luận 
@app.route('/post/<int:post_id>', methods=['GET', 'POST'])
def post_detail(post_id):
    conn = get_db_connection()
    post = conn.execute(
        'SELECT posts.*, users.username FROM posts JOIN users ON posts.user_id = users.id WHERE posts.id = ?',
        (post_id,)
    ).fetchone()

    if request.method == 'POST' and 'user_id' in session:
        content = request.form['comment']
        conn.execute(
            'INSERT INTO comments (content, post_id, user_id) VALUES (?, ?, ?)',
            (content, post_id, session['user_id'])
        )
        conn.commit()

    comments = conn.execute(
        'SELECT comments.*, users.username FROM comments JOIN users ON comments.user_id = users.id WHERE post_id = ?',
        (post_id,)
    ).fetchall()

    conn.close()
    return render_template('post_detail.html', post=post, comments=comments)

# Edit
@app.route('/edit/<int:post_id>', methods=['GET', 'POST'])
def edit_post(post_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))

    conn = get_db_connection()
    post = conn.execute('SELECT * FROM posts WHERE id = ?', (post_id,)).fetchone()

    if not post:
        flash('Post not found!')
        return redirect(url_for('index'))

    if post['user_id'] != session['user_id']:
        flash('You are not authorized to edit this post!')
        return redirect(url_for('index'))

    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        image = post['image']

        if 'image' in request.files:
            file = request.files['image']
            if file.filename:
                filename = secure_filename(file.filename)
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(filepath)
                image = filename

        conn.execute(
            'UPDATE posts SET title=?, content=?, image=? WHERE id=?',
            (title, content, image, post_id)
        )
        conn.commit()
        conn.close()
        flash('Post updated successfully!')
        return redirect(url_for('post_detail', post_id=post_id))

    conn.close()
    return render_template('edit.html', post=post)

# Delete
@app.route('/delete/<int:post_id>', methods=['POST'])
def delete_post(post_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))

    conn = get_db_connection()
    post = conn.execute('SELECT * FROM posts WHERE id = ?', (post_id,)).fetchone()

    if post and post['user_id'] == session['user_id']:
        conn.execute('DELETE FROM posts WHERE id = ?', (post_id,))
        conn.commit()
        flash('Post deleted successfully!')
    else:
        flash('You are not authorized to delete this post.')

    conn.close()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
