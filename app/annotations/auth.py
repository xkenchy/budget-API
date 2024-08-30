import jwt
from flask import request, jsonify
from functools import wraps
from datetime import datetime
import os

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')

        if not token:
            return jsonify({'message': 'Token is missing!'}), 401

        # Strip the 'Bearer ' prefix from the token
        if token.startswith('Bearer '):
            token = token[len('Bearer '):]

        try:
            payload = jwt.decode(token, os.getenv('SECRET_KEY'), algorithms=['HS256'])
            if payload['exp'] < datetime.utcnow().timestamp():
                return jsonify({'message': 'Token has expired!'}), 401
        except jwt.ExpiredSignatureError:
            return jsonify({'message': 'Token has expired!'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'message': 'Invalid token!'}), 401

        return f(*args, **kwargs)

    return decorated
