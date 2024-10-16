"""Praxisprojekt: Book Reviewer - Lutz Celina"""


from flask import Blueprint, jsonify, request
from flask_login import login_required, current_user

from review import Review
from reviewdao import ReviewDao

review_blueprint = Blueprint('review_blueprint', __name__)
review_dao = ReviewDao('book_review.db')


@review_blueprint.route('/books/<int:book_id>/reviews', methods=['GET'])
@login_required
def get_all_reviews(book_id):
    items = review_dao.get_all_items(book_id)
    return jsonify([item.__dict__ for item in items]), 200

@review_blueprint.route('/books/<int:book_id>/reviews/<int:review_id>', methods=['GET'])
@login_required
def get_review(review_id, book_id):
    item = review_dao.get_item(review_id, book_id)
    if item:
        return jsonify(item.__dict__), 200
    else:
        return jsonify({'message': 'Review not found'}), 404

@review_blueprint.route('/books/<int:book_id>/reviews', methods=['POST'])
@login_required
def add_review(book_id):
    data = request.get_json()
    new_item = Review(None, current_user.id, book_id, data['rating'], data['comment'], data['review_date'])
    review_dao.add_item(new_item)
    return jsonify({'message': 'Review added'}), 201

@review_blueprint.route('/books/<int:book_id>/reviews/<int:review_id>', methods=['PUT'])
@login_required
def update_review(review_id, book_id):
    data = request.get_json()
    updated_item = Review(
        review_id, current_user, book_id, data['rating'], data['comment'], data['review_date']
    )
    if review_dao.update_item(updated_item):
        return jsonify({'message': 'Review updated'}), 200
    else:
        return jsonify({'message': 'Review not found or not updated'}), 404

@review_blueprint.route('/books/<int:book_id>/reviews/<int:review_id>', methods=['DELETE'])
@login_required
def delete_review(review_id, book_id):
    if review_dao.delete_item(review_id, book_id):
        return jsonify({'message': 'Review deleted'}), 200
    else:
        return jsonify({'message': 'Review not found or not deleted'}), 404
