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
    users = [(1, 'user1', 'user1@example', 'pass', False),
             (2, 'user2', 'user2@example', 'pass', True),
             (3, 'user3', 'user3@example', 'pass', False),
             (4, 'user4', 'user4@example', 'pass', False),
             (5, 'user5', 'user5@example', 'pass', False)]

    for user in users:
        user_dao.add_user(User(*user))

    # Generate books
    books = [(1, 'book1', 'Author 1', '11.11.2020', 1, 10.00),
             (2, 'book2', 'Author 2', '12.11.2020', 1, 20.00),
             (3, 'book3', 'Author 3', '12.11.2020', 1, 30.00),
             (4, 'book4', 'Author 3', '12.11.2020', 1, 30.00),
             (5, 'book5', 'Author 3', '12.11.2020', 1, 50.00),
             (6, 'book6', 'Author 2', '12.11.2020', 1, 100.00),
             (7, 'book7', 'Author 2', '12.11.2020', 1, 10.00)]

    for book in books:
        book_dao.add_item(Book(*book))

    # Generate reviews
    reviews = [(1, 1, 1, 1, 'sehr schlecht', '11.11.2020'),
               (2, 2, 1, 1, 'sehr schlecht', '12.11.2021'),
               (3, 1, 2, 3, 'okay', '13.11.2020'),
               (4, 2, 3, 4, 'gut', '11.11.2021'),
               (5, 2, 3, 1, 'sehr schlecht', '11.11.2021'),
               (6, 3, 5, 1, 'sehr schlecht', '11.11.2005'),
               (7, 3, 4, 5, 'sehr gut', '11.11.2020'),
               (8, 3, 2, 2, 'schlecht', '11.11.2020'),
               (9, 2, 1, 1, 'sehr schlecht', '11.11.2020'),
               (10, 2, 3, 1, 'sehr schlecht', '11.11.2015'),
               (11, 5, 4, 2, 'schlecht', '11.11.2020'),
               (12, 5, 1, 5, 'sehr gut', '11.11.2020'),
               (13, 6, 3, 1, 'sehr schlecht', '11.11.2013'),
               (14, 7, 2, 5, 'sehr gut', '11.11.2018'),
               (15, 7, 5, 3, 'okay', '11.11.2022')]


    for review in reviews:
        review_dao.add_item(Review(*review))




if __name__ == '__main__':
    generate_testdata()

    app.run(debug=True)
