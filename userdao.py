"""Praxisprojekt: Book Reviewer - Lutz Celina"""


import sqlite3
import bcrypt
from user import User


class UserDao:
    """UserDao class"""

    def __init__(self, db_file):
        self.conn = sqlite3.connect(db_file, check_same_thread=False)
        self.cursor = self.conn.cursor()

    def create_table(self):
        self.cursor.execute("""DROP TABLE IF EXISTS users""")
        self.cursor.execute(
            """CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username TEXT, email TEXT, password TEXT, is_admin BOOLEAN)"""
        )
        self.conn.commit()

    def add_user(self, user):
        hashed_pass = bcrypt.hashpw(user.password.encode("utf-8"), bcrypt.gensalt())
        self.cursor.execute(
            "INSERT INTO users (username, email, password, is_admin) VALUES (?, ?, ?, ?)",
            (user.username, user.email, hashed_pass, user.is_admin),
        )
        self.conn.commit()

    def get_user_by_id(self, user_id):
        self.cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
        row = self.cursor.fetchone()
        if row:
            return User(row[0], row[1], row[2], row[3], row[4])
        return None

    def get_user_by_username(self, username):
        self.cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
        row = self.cursor.fetchone()
        if row:
            return User(row[0], row[1], row[2], row[3], row[4])
        return None

    def delete_user(self, user_id):
        self.cursor.execute("DELETE FROM users WHERE id = ?", (user_id,))
        if self.cursor.rowcount > 0:
            self.conn.commit()
            return True
        return False

    def update_user(self, user):
        self.cursor.execute(
            "UPDATE users SET username = ?, email = ?, password = ?, is_admin = ? WHERE id = ?",
            (user.username, user.email, user.password, user.is_admin, user.id),
        )
        if self.cursor.rowcount > 0:
            self.conn.commit()
            return True
        return False

    def get_all_users(self):
        self.cursor.execute("SELECT * FROM users")
        rows = self.cursor.fetchall()
        items = [User(row[0], row[1], row[2], row[3], row[4]) for row in rows]
        return items



    def close(self):
        self.conn.close()