"""Praxisprojekt: Book Reviewer - Lutz Celina"""


from flask import Blueprint, jsonify, request
from flask_login import login_required, current_user

from book import Book
from bookdao import BookDao

book_blueprint = Blueprint('book_blueprint', __name__)
book_dao = BookDao('book_review.db')

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
def add_book():
    data = request.get_json()
    new_item = Book(None, data['title'], data['author'], data['release_date'], None)
    book_dao.add_item(new_item)
    return jsonify({'message': 'Book added'}), 201

@book_blueprint.route('/books/<int:book_id>', methods=['PUT'])
def update_book(book_id):
    data = request.get_json()
    updated_item = Book(
        book_id, data['title'], data['author'], data['release_date'], data['average_rating']
    )
    if book_dao.update_item(updated_item):
        return jsonify({'message': 'Book updated'}), 200
    else:
        return jsonify({'message': 'Book not found or not updated'}), 404

@book_blueprint.route('/books/<int:book_id>', methods=['DELETE'])
def delete_book(book_id):
    if book_dao.delete_item(book_id):
        return jsonify({'message': 'Book deleted'}), 200
    else:
        return jsonify({'message': 'Book not found or not deleted'}), 404