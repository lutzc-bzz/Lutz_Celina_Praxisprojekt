"""Praxisprojekt: Book Reviewer - Lutz Celina"""


import bcrypt
from flask import Blueprint, request, jsonify
from flask_login import login_required, login_user, logout_user
from userdao import UserDao
from user import User

user_blueprint = Blueprint('user_blueprint', __name__)
user_dao = UserDao('book_review.db')


@user_blueprint.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = user_dao.get_user_by_username(data['username'])
    if user and bcrypt.checkpw(data['password'].encode('utf-8'), user.password):
        login_user(user)
        return jsonify({'success': True}), 200
    return jsonify({'error': 'Invalid username or password'}), 401

@user_blueprint.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    new_user = User(None, data['username'], data['email'], data['password'], False)
    user_dao.add_user(new_user)
    return jsonify({'success': True}), 200

@user_blueprint.route('/logout')
@login_required
def logout():
    logout_user()
    return jsonify({'success': True}), 200

def check_state(string):
    if string == 'True':
        return True
    if string == 'False':
        return False
    else:
        return None

def change_user_status(object, state):
    object.admin = state
    return object

@user_blueprint.route('/changeadminstatus', methods=['POST'])
def change_admin_status():
    data = request.get_json()
    user = user_dao.get_user_by_username(data['username'])
    if user and check_state(data['admin']) is not None:
        user_dao.update_user(change_user_status(user, check_state(data['admin'])))
        return jsonify({'message': 'User admin status changed'}), 200
    if user is None:
        return jsonify({'error': 'Invalid username'}), 401
    return jsonify({'error': 'Invalid admin state'}), 401
