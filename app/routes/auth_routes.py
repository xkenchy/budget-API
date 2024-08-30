import os
import jwt
from datetime import datetime, timedelta
from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from services.auth_service import create_user, find_user_by_username
from annotations.auth import token_required

auth_bp = Blueprint('auth_bp', __name__)

@auth_bp.route('/create', methods=['POST'])
def signup():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    email = data.get('email')

    if not username or not password or not email:
        return jsonify({'message': 'Username, password, and email are required!'}), 400

    # Hash the password before storing it
    password_hash = generate_password_hash(password)

    # Call the service function to create the user
    result = create_user(username, password_hash, email)

    if result['status'] == 'success':
        return jsonify({'message': 'User created successfully!'}), 201
    else:
        return jsonify({'message': result['message']}), 400

@auth_bp.route('/signin', methods=['POST'])
def signin():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({'message': 'Username and password are required!'}), 400

    # Find the user by username
    user = find_user_by_username(username)

    if user and check_password_hash(user['password_hash'], password):
        # Password matches, create a JWT token
        token = jwt.encode(
            {
                'username': username,
                'exp': datetime.utcnow() + timedelta(hours=6)  # Token expires in 1 hour
            },
            os.getenv('SECRET_KEY'),  # Use your secret key
            algorithm='HS256'
        )
        return jsonify({'token': token}), 200
    else:
        return jsonify({'message': 'Invalid credentials'}), 401
