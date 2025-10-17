import os
import sqlite3
from flask import Flask, render_template, request, redirect, url_for, flash

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "library.db")
SCHEMA_PATH = os.path.join(BASE_DIR, "schema.sql")

app = Flask(__name__)
app.secret_key = "very-secret-key"  # đổi khi deploy

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    if not os.path.exists(DB_PATH):
        with sqlite3.connect(DB_PATH) as conn:
            with open(SCHEMA_PATH, "r", encoding="utf-8") as f:
                conn.executescript(f.read())
        print("Database initialized.")

@app.route("/initdb")
def initdb_route():
    init_db()
    return "Database initialized."

# Home: list books with search
@app.route("/", methods=["GET"])
def index():
    q = request.args.get("q", "").strip()
    conn = get_db()
    if q:
        like = f"%{q}%"
        books = conn.execute(
            "SELECT * FROM books WHERE title LIKE ? OR author LIKE ? OR isbn LIKE ? ORDER BY title",
            (like, like, like),
        ).fetchall()
    else:
        books = conn.execute("SELECT * FROM books ORDER BY title").fetchall()
    conn.close()
    return render_template("index.html", books=books, q=q)

# Add book
@app.route("/book/add", methods=["GET", "POST"])
def add_book():
    if request.method == "POST":
        title = request.form.get("title", "").strip()
        author = request.form.get("author", "").strip()
        isbn = request.form.get("isbn", "").strip()
        qty = int(request.form.get("quantity", 0))

        if not title:
            flash("Title is required.", "danger")
            return redirect(url_for("add_book"))

        conn = get_db()
        try:
            conn.execute(
                "INSERT INTO books (title, author, isbn, quantity) VALUES (?, ?, ?, ?)",
                (title, author or None, isbn or None, qty),
            )
            conn.commit()
            flash("Book added.", "success")
        except sqlite3.IntegrityError:
            flash("ISBN already exists.", "warning")
        finally:
            conn.close()
        return redirect(url_for("index"))
    return render_template("add_book.html")

# Edit book
@app.route("/book/<int:book_id>/edit", methods=["GET", "POST"])
def edit_book(book_id):
    conn = get_db()
    book = conn.execute("SELECT * FROM books WHERE id = ?", (book_id,)).fetchone()
    if not book:
        conn.close()
        flash("Book not found.", "danger")
        return redirect(url_for("index"))

    if request.method == "POST":
        title = request.form.get("title", "").strip()
        author = request.form.get("author", "").strip()
        isbn = request.form.get("isbn", "").strip()
        qty = int(request.form.get("quantity", 0))

        if not title:
            flash("Title required.", "danger")
            return redirect(url_for("edit_book", book_id=book_id))

        try:
            conn.execute(
                "UPDATE books SET title=?, author=?, isbn=?, quantity=? WHERE id=?",
                (title, author or None, isbn or None, qty, book_id),
            )
            conn.commit()
            flash("Book updated.", "success")
        except sqlite3.IntegrityError:
            flash("ISBN conflict.", "warning")
        finally:
            conn.close()
        return redirect(url_for("index"))

    conn.close()
    return render_template("edit_book.html", book=book)

# Delete book
@app.route("/book/<int:book_id>/delete", methods=["POST"])
def delete_book(book_id):
    conn = get_db()
    conn.execute("DELETE FROM books WHERE id=?", (book_id,))
    conn.commit()
    conn.close()
    flash("Book deleted.", "info")
    return redirect(url_for("index"))

# Borrow / Return page
@app.route("/book/<int:book_id>/borrow", methods=["GET", "POST"])
def borrow_book(book_id):
    conn = get_db()
    book = conn.execute("SELECT * FROM books WHERE id = ?", (book_id,)).fetchone()
    if not book:
        conn.close()
        flash("Book not found.", "danger")
        return redirect(url_for("index"))

    if request.method == "POST":
        action = request.form.get("action")  # 'borrow' or 'return'
        borrower = request.form.get("borrower", "").strip()
        qty = int(request.form.get("qty", 1))
        if qty <= 0:
            flash("Quantity must be >= 1", "warning")
            return redirect(url_for("borrow_book", book_id=book_id))

        if action == "borrow":
            if book["quantity"] < qty:
                flash("Not enough copies available.", "warning")
                conn.close()
                return redirect(url_for("borrow_book", book_id=book_id))
            # reduce quantity
            conn.execute("UPDATE books SET quantity = quantity - ? WHERE id = ?", (qty, book_id))
            conn.execute(
                "INSERT INTO transactions (book_id, action, borrower_name, qty) VALUES (?, ?, ?, ?)",
                (book_id, "borrow", borrower or None, qty),
            )
            conn.commit()
            flash(f"Borrowed {qty} copy(ies).", "success")

        elif action == "return":
            conn.execute("UPDATE books SET quantity = quantity + ? WHERE id = ?", (qty, book_id))
            conn.execute(
                "INSERT INTO transactions (book_id, action, borrower_name, qty) VALUES (?, ?, ?, ?)",
                (book_id, "return", borrower or None, qty),
            )
            conn.commit()
            flash(f"Returned {qty} copy(ies).", "success")

        conn.close()
        return redirect(url_for("index"))

    conn.close()
    return render_template("borrow.html", book=book)

# Transactions / history
@app.route("/history")
def history():
    conn = get_db()
    rows = conn.execute(
        "SELECT t.*, b.title FROM transactions t JOIN books b ON t.book_id = b.id ORDER BY t.created_at DESC"
    ).fetchall()
    conn.close()
    return render_template("history.html", rows=rows)

if __name__ == "__main__":
    init_db()
    app.run(debug=True, use_reloader=False)
