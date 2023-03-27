from flask import Blueprint, request, jsonify
from services.mongodb import MongoDB
from services.hashing import hash_password, verify_password

user_db = MongoDB('general', 'users')
auth_bp = Blueprint('auth', __name__, url_prefix='/auth')


@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data['email']
    password = data['password']

    if doc:=user_db.Query_One({'email': email, 'password': hash_password(password)}):
        return jsonify({'success': True}, {'result': doc})
    else:
        return jsonify({'success': False})


@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    email = data['email']
    password = data['password']

    if user_db.Query_One({'email': email}):
        return jsonify({'success': False, 'message': 'Username already exists.'})
    
    user_db.Insert_One({'email': email, 'password': hash_password(password)})
    return jsonify({'success': True})


@auth_bp.route('/logout', methods=['POST'])
def logout():
    return jsonify({'success': True})