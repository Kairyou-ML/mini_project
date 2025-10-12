import sqlite3

# Tạo kết nối với file database
connection = sqlite3.connect('blog.db')

# Đọc nội dung file schema.sql và chạy
with open('schema.sql', 'r', encoding='utf-8') as f:
    connection.executescript(f.read())

connection.commit()
connection.close()

print("Database created successfully with users, posts, and comments tables!")
