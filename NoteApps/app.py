import os
import sqlite3
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import (
    LoginManager, UserMixin, login_user, login_required,
    logout_user, current_user
)
from werkzeug.security import generate_password_hash, check_password_hash

# Cấu hình
app = Flask(__name__)
app.secret_key = 'secretkey'
DATABASE = 'notes.db'

# Flask-Login 
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# User Model
class User(UserMixin):
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password

# DB helper 
def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    with sqlite3.connect(DATABASE) as conn:
        with open('schema.sql', 'r') as f:
            conn.executescript(f.read())

# Login
@login_manager.user_loader
def load_user(user_id):
    conn = get_db()
    user = conn.execute('SELECT * FROM users WHERE id = ?', (user_id,)).fetchone()
    conn.close()
    if user:
        return User(user['id'], user['username'], user['password'])
    return None

@app.route('/initdb')
def initdb():
    init_db()
    return "Database initialized!"

#  Routes
@app.route('/')
@login_required
def index():
    conn = get_db()
    notes = conn.execute(
        'SELECT * FROM notes WHERE user_id = ? ORDER BY created_at DESC',
        (current_user.id,)
    ).fetchall()
    conn.close()
    return render_template('index.html', notes=notes)

# Register
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = generate_password_hash(request.form['password'])
        conn = get_db()
        try:
            conn.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, password))
            conn.commit()
            flash('Đăng ký thành công! Đăng nhập ngay nhé.')
            return redirect(url_for('login'))
        except sqlite3.IntegrityError:
            flash('Tên đăng nhập đã tồn tại!')
        finally:
            conn.close()
    return render_template('register.html')


# Login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        conn = get_db()
        user = conn.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()
        conn.close()
        if user and check_password_hash(user['password'], password):
            login_user(User(user['id'], user['username'], user['password']))
            return redirect(url_for('index'))
        flash('Sai tên đăng nhập hoặc mật khẩu!')
    return render_template('login.html')

# Logout
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

# Add
@app.route('/create', methods=['GET', 'POST'])
@login_required
def create_note():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        conn = get_db()
        conn.execute(
            'INSERT INTO notes (title, content, user_id) VALUES (?, ?, ?)',
            (title, content, current_user.id)
        )
        conn.commit()
        conn.close()
        flash('Ghi chú đã được lưu!')
        return redirect(url_for('index'))
    return render_template('create_note.html')

@app.route('/note/<int:note_id>')
@login_required
def note_detail(note_id):
    conn = get_db()
    note = conn.execute(
        'SELECT * FROM notes WHERE id = ? AND user_id = ?',
        (note_id, current_user.id)
    ).fetchone()
    conn.close()
    if not note:
        flash('Không tìm thấy ghi chú!')
        return redirect(url_for('index'))
    return render_template('note_detail.html', note=note)

# Edit
@app.route('/edit/<int:note_id>', methods=['GET', 'POST'])
@login_required
def edit_note(note_id):
    conn = get_db()
    note = conn.execute(
        'SELECT * FROM notes WHERE id = ? AND user_id = ?',
        (note_id, current_user.id)
    ).fetchone()
    if not note:
        flash('Không tìm thấy ghi chú!')
        return redirect(url_for('index'))

    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        conn.execute(
            'UPDATE notes SET title=?, content=? WHERE id=? AND user_id=?',
            (title, content, note_id, current_user.id)
        )
        conn.commit()
        conn.close()
        flash('Cập nhật thành công!')
        return redirect(url_for('index'))

    conn.close()
    return render_template('edit_note.html', note=note)

@app.route('/delete/<int:note_id>', methods=['POST'])
@login_required
def delete_note(note_id):
    conn = get_db()
    conn.execute('DELETE FROM notes WHERE id=? AND user_id=?', (note_id, current_user.id))
    conn.commit()
    conn.close()
    flash('Đã xóa ghi chú!')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True, use_reloader=False)
