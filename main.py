"""Praxisprojekt: Book Reviewer - Lutz Celina"""
from random import randint

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
    users = [(1, 'user1', 'user1@example', 'pass', True),
              (2, 'user2', 'user2@example', 'pass', False),]

    for c in range(3, 6):
        users.append((c, f'user{c}', f'user{c}@example', 'pass', randint(0, 1)))


    for user in users:
        user_dao.add_user(User(*user))

    # Generate books
    books = []

    for c in range(1, 8):
        books.append((c, f'book{c}', f'Author {c}', '11.11.2020', 1, float(randint(0, 200))))

    for book in books:
        book_dao.add_item(Book(*book))

    # Generate reviews
    reviews = []
    comments = ['sehr schlecht', 'schlecht', 'okay', 'gut', 'sehr gut']

    for c in range(1, 16):
        rating = randint(1, 5)
        reviews.append((c, randint(1, 7), randint(1, 5), rating, comments[rating - 1], '11.11.2020'))

    for review in reviews:
        review_dao.add_item(Review(*review))


if __name__ == '__main__':
    generate_testdata()

    app.run(debug=True)
