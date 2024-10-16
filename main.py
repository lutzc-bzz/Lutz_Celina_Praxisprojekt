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


def generate_testdata():
    user_dao = UserDao('book_review.db')
    book_dao = BookDao('book_review.db')
    review_dao = ReviewDao('book_review.db')

    # Generate users
    user_dao.create_table()
    user_dao.add_user(User(1, 'user1', 'user1@example', 'pass1'))
    user_dao.add_user(User(2, 'user2', 'user2@example', 'pass2'))

    # Generate books
    book_dao.create_table()
    book_dao.add_item(Book(1, 'book1', 'Author 1', '11.11.2020', 1))
    book_dao.add_item(Book(2, 'book2', 'Author 2', '12.11.2020', 1))
    book_dao.add_item(Book(3, 'book3', 'Author 3', '13.11.2020', 1))
    book_dao.add_item(Book(4, 'book4', 'Author 1', '11.11.2020', 1))
    book_dao.add_item(Book(5, 'book5', 'Author 2', '11.11.2020', 1))

    # Generate reviews
    review_dao.create_table()
    review_dao.add_item(Review(1, 1, 1, 1, 'sehr schlecht', '11.11.2020'))
    review_dao.add_item(Review(2, 2, 1, 2, 'schlecht', '12.11.2020'))
    review_dao.add_item(Review(3, 1, 2, 3, 'gut', '13.11.2020'))
    review_dao.add_item(Review(4, 2, 2, 4, 'sehr gut', '11.11.2020'))
    review_dao.add_item(Review(5, 1, 3, 5, 'super', '13.11.2020'))
    review_dao.add_item(Review(6, 2, 3, 1, 'sehr schlecht', '11.11.2020'))


if __name__ == '__main__':
    generate_testdata()
    app.run(debug=True)
