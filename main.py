"""Praxisprojekt: Book Reviewer - Lutz Celina"""

from flask import Flask
from flask_login import LoginManager

import bookblueprint
import reviewblueprint
import userblueprint
from book import Book
from bookdao import BookDao
from review import Review
from user import User
from userdao import UserDao
from reviewdao import ReviewDao

app = Flask(__name__)
app.secret_key = 'supersecretkey'

login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    user_dao = UserDao('book_review.db')
    return user_dao.get_user_by_id(int(user_id))


app.register_blueprint(userblueprint.user_blueprint)
app.register_blueprint(bookblueprint.book_blueprint)
app.register_blueprint(reviewblueprint.review_blueprint)

db = 'book_review.db'
user_dao = UserDao(db)
book_dao = BookDao(db)
review_dao = ReviewDao(db)

def create_tables():
    user_dao.create_table()
    book_dao.create_table()
    review_dao.create_table()

def generate_testdata():
    create_tables()

    # Generate users
    users = [(1, 'user1', 'user1@example', 'pass1', False),
             (2, 'user2', 'user2@example', 'pass2', True)]

    for user in users:
        user_dao.add_user(User(*user))

    # Generate books
    books = [(1, 'book1', 'Author 1', '11.11.2020', 1, 10.00),
             (2, 'book2', 'Author 2', '12.11.2020', 1, 10.00)]

    for book in books:
        book_dao.add_item(Book(*book))

    # Generate reviews
    reviews = [(1, 1, 1, 1, 'sehr schlecht', '11.11.2020'),
               (2, 2, 1, 1, 'schlecht', '12.11.2020'),
               (3, 1, 2, 1, 'gut', '13.11.2020'),
               (4, 2, 2, 1, 'sehr gut', '11.11.2020')]


    for review in reviews:
        review_dao.add_item(Review(*review))


if __name__ == '__main__':
    generate_testdata()

    app.run(debug=True)
