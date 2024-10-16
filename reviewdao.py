"""Praxisprojekt: Book Reviewer - Lutz Celina"""


import sqlite3
from review import Review


class ReviewDao:

    def __init__(self, db_file):
        self.conn = sqlite3.connect(db_file, check_same_thread=False)
        self.cursor = self.conn.cursor()

    def create_table(self):
        self.cursor.execute("""DROP TABLE IF EXISTS reviews""")
        self.cursor.execute(
            """CREATE TABLE IF NOT EXISTS reviews (
                review_id INTEGER PRIMARY KEY,
                user_id INTEGER,
                book_id INTEGER,
                rating INTEGER,
                comment TEXT,
                review_date TEXT
                )"""
        )
        self.conn.commit()

    def add_item(self, review):
        self.cursor.execute(
            "INSERT INTO reviews (user_id, book_id, rating, comment, review_date) VALUES (?, ?, ?, ?, ?)",
            (review.user_id, review.book_id, review.rating, review.comment , review.review_date),
        )
        self.conn.commit()

    def get_item(self, review_id, book_id):
        self.cursor.execute(
            "SELECT * FROM reviews WHERE review_id = ? AND book_id = ?", (review_id, book_id),
        )
        row = self.cursor.fetchone()
        if row:
            return Review(row[0], row[1], row[2], row[3], row[4], row[5])
        return None

    def get_all_items(self, book_id):
        self.cursor.execute("SELECT * FROM reviews WHERE book_id = ?", (book_id,))
        rows = self.cursor.fetchall()
        items = [Review(row[0], row[1], row[2], row[3], row[4], row[5]) for row in rows]
        return items

    def update_item(self, review):
        self.cursor.execute(
            "UPDATE reviews SET user_id = ?, book_id = ?, rating = ?, comment = ?, review_date = ? WHERE review_id = ?",
            (review.user_id, review.book_id, review.rating, review.comment, review.review_date, review.review_id),
        )
        if self.cursor.rowcount > 0:
            self.conn.commit()
            return True
        return False

    def delete_item(self, review_id, book_id):
        self.cursor.execute(
            "DELETE FROM reviews WHERE review_id = ? AND book_id = ?", (review_id, book_id),
        )
        if self.cursor.rowcount > 0:
            self.conn.commit()
            return True
        return False

    def close(self):
        self.conn.close()
