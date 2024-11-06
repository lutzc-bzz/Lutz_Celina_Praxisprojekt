"""Praxisprojekt: Book Reviewer - Lutz Celina"""

from flask import Blueprint, jsonify, request
from flask_login import login_required, current_user

from userdao import UserDao
from book import Book
from bookdao import BookDao
from reviewdao import ReviewDao

book_blueprint = Blueprint('book_blueprint', __name__)
review_dao = ReviewDao('book_review.db')
book_dao = BookDao('book_review.db')
user_dao = UserDao('book_review.db')

def calculate_average(list):
    total = 0
    count = 0
    for item in list:
        total += item.rating
        count += 1

    return int(total / count)

def discount_price(discount):
    def calculate_price(book):
        return book.price * discount
    return calculate_price


@book_blueprint.route('/books', methods=['GET'])
def get_all_books():
    items = book_dao.get_all_items()
    return jsonify([item.__dict__ for item in items]), 200


@book_blueprint.route('/books/<int:book_id>', methods=['GET'])
def get_item(book_id):
    item = book_dao.get_item(book_id)
    if item:
        return jsonify(item.__dict__), 200
    else:
        return jsonify({'message': 'Book not found'}), 404


@book_blueprint.route('/books', methods=['POST'])
@login_required
def add_book():
    data = request.get_json()
    new_item = Book(None, data['title'], data['author'], data['release_date'], 1, data['price'])
    user = user_dao.get_user_by_id(current_user.id)
    if user.is_admin:
        book_dao.add_item(new_item)
        return jsonify({'message': 'Book added'}), 201
    return jsonify({'message': 'User does not have corresponding access'}), 403


@book_blueprint.route('/books/<int:book_id>', methods=['PUT'])
@login_required
def update_book(book_id):
    data = request.get_json()
    updated_item = Book(
        book_id, data['title'], data['author'], data['release_date'], data['average_rating'], data['price']
    )
    user = user_dao.get_user_by_id(current_user.id)
    if user.is_admin:
        if book_dao.update_item(updated_item):
            return jsonify({'message': 'Book updated'}), 200
        return jsonify({'message': 'Book not found or not updated'}), 404
    return jsonify({'message': 'User does not have corresponding access'}), 403

@book_blueprint.route('/books/<int:book_id>/discount', methods=['PUT'])
@login_required
def discount_book(book_id):
    data = request.get_json()
    book = book_dao.get_item(book_id)
    discount = discount_price(data['discount'])
    book.price = discount(book)
    updated_item = book
    user = user_dao.get_user_by_id(current_user.id)
    if user.is_admin:
        if book_dao.update_item(updated_item):
            return jsonify({'message': 'Book updated'}), 200
        return jsonify({'message': 'Book not found or not updated'}), 404
    return jsonify({'message': 'User does not have corresponding access'}), 403

@book_blueprint.route('/books/<int:book_id>', methods=['PUT'])
@login_required
def update_average_rating(book_id):
    data = request.get_json()
    # Berechne durschnittliche Bewertung vom Buch
    reviews = review_dao.get_all_items_by_book_id(book_id)
    average_rating = calculate_average(reviews)

    # Aktualisiere average_rating vom Buch
    updated_item = Book(
        book_id, data['title'], data['author'], data['release_date'], average_rating
    )
    if book_dao.update_item(updated_item):
        return jsonify({'message': 'Book updated'}), 200
    return jsonify({'message': 'Book not found or not updated'}), 404


@book_blueprint.route('/books/<int:book_id>', methods=['DELETE'])
@login_required
def delete_book(book_id):
    user = user_dao.get_user_by_id(current_user.id)
    if user.is_admin:
        if book_dao.delete_item(book_id):
            return jsonify({'message': 'Book deleted'}), 200
        else:
            return jsonify({'message': 'Book not found or not deleted'}), 404
    return jsonify({'message': 'User does not have corresponding access'}), 403
