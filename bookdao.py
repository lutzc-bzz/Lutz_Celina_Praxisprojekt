"""Praxisprojekt: Book Reviewer - Lutz Celina"""


import sqlite3
from book import Book


class BookDao:

    def __init__(self, db_file):
        self.conn = sqlite3.connect(db_file, check_same_thread=False)
        self.cursor = self.conn.cursor()

    def create_table(self):
        self.cursor.execute("""DROP TABLE IF EXISTS books""")
        self.cursor.execute(
            """CREATE TABLE IF NOT EXISTS books (
                book_id INTEGER PRIMARY KEY,
                title TEXT,
                author TEXT,
                release_date TEXT,
                average_rating INTEGER
                )"""
        )
        self.conn.commit()

    def add_item(self, book):
        self.cursor.execute(
            "INSERT INTO books (title, author, release_date, average_rating) VALUES (?, ?, ?, ?)",
            (book.title, book.author, book.release_date, book.average_rating),
        )
        self.conn.commit()

    def get_item(self, book_id):
        self.cursor.execute(
            "SELECT * FROM books WHERE book_id = ?",
            (book_id,),
        )
        row = self.cursor.fetchone()
        if row:
            return Book(row[0], row[1], row[2], row[3], row[4])
        return None

    def get_all_items(self):
        self.cursor.execute("SELECT * FROM books")
        rows = self.cursor.fetchall()
        items = [Book(row[0], row[1], row[2], row[3], row[4]) for row in rows]
        return items

    def update_item(self, book):
        self.cursor.execute(
            "UPDATE books SET title = ?, author = ?, release_date = ?, average_rating = ? WHERE book_id = ?",
            (book.title, book.author, book.release_date, book.average_rating, book.book_id),
        )
        if self.cursor.rowcount > 0:
            self.conn.commit()
            return True
        return False

    def delete_item(self, book_id):
        self.cursor.execute(
            "DELETE FROM books WHERE book_id = ?",
            (book_id,),
        )
        if self.cursor.rowcount > 0:
            self.conn.commit()
            return True
        return False

    def close(self):
        self.conn.close()