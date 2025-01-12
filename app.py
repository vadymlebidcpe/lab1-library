import os
import psycopg2
from flask import Flask, render_template, request, redirect, url_for
import logging

app = Flask(__name__)

# Настройка логирования
LOG_FILE_PATH = '/var/log/app/app.log'
os.makedirs(os.path.dirname(LOG_FILE_PATH), exist_ok=True)
logging.basicConfig(
    filename=LOG_FILE_PATH,
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s]: %(message)s'
)

DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise ValueError("DATABASE_URL is not set. Please configure it in the environment variables.")

# Инициализация базы данных (создание таблицы)
def init_db():
    try:
        logging.info("Initializing database...")
        conn = psycopg2.connect(DATABASE_URL)
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS books (
                id SERIAL PRIMARY KEY,
                title TEXT NOT NULL,
                author TEXT NOT NULL
            );
        """)
        conn.commit()
        cursor.close()
        conn.close()
        logging.info("Database initialized successfully")
    except Exception as e:
        logging.error(f"Error initializing database: {e}")

# Главная страница с таблицей книг
@app.route('/')
def index():
    try:
        conn = psycopg2.connect(DATABASE_URL)
        cursor = conn.cursor()
        cursor.execute("SELECT id, title, author FROM books;")
        books = cursor.fetchall()
        cursor.close()
        conn.close()
        logging.info("Accessed main page and fetched books")
        return render_template('index.html', books=books)
    except Exception as e:
        logging.error(f"Error fetching books: {e}")
        return "Error fetching books", 500

# Добавить книгу
@app.route('/add', methods=['POST'])
def add_book():
    title = request.form['title']
    author = request.form['author']
    
    try:
        conn = psycopg2.connect(DATABASE_URL)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO books (title, author) VALUES (%s, %s);", (title, author))
        conn.commit()
        cursor.close()
        conn.close()
        logging.info(f"Added book: {title} by {author}")
    except Exception as e:
        logging.error(f"Error adding book: {e}")
    
    return redirect(url_for('index'))

# Удалить книгу
@app.route('/delete/<int:book_id>', methods=['POST'])
def delete_book(book_id):
    try:
        conn = psycopg2.connect(DATABASE_URL)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM books WHERE id = %s;", (book_id,))
        conn.commit()
        cursor.close()
        conn.close()
        logging.info(f"Deleted book with ID: {book_id}")
    except Exception as e:
        logging.error(f"Error deleting book with ID {book_id}: {e}")
    
    return redirect(url_for('index'))

if __name__ == '__main__':
    # Вызываем init_db перед запуском приложения
    init_db()
    logging.info("Starting Flask application")
    app.run(host='0.0.0.0', port=5000)
