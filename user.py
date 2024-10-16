"""Praxisprojekt: Book Reviewer - Lutz Celina"""


from flask_login import UserMixin


class User(UserMixin):

    def __init__(self, user_id, username, email, password, is_admin):
        self.id = user_id
        self.username = username
        self.email = email
        self.password = password
        self.is_admin = is_admin
