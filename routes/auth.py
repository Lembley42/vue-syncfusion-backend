from flask import Blueprint, request, jsonify, make_response
from services.mongodb import MongoDB
from services.hashing import hash_password, verify_password


user_db = MongoDB('general', 'users')
auth_bp = Blueprint('auth', __name__, url_prefix='/auth')


# 400 - Bad request (missing email or password)
# 401 - Unauthorized (invalid email or password)
# 200 - OK (user logged in)
@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()

    if 'email' not in data or 'password' not in data:
        return make_response(jsonify({'success': False, 'message': 'Invalid request.'}), 400)

    email = data['email']
    password = data['password']

    if doc:=user_db.Query_One({'email': email, 'password': hash_password(password)}):
        return make_response(jsonify({'success': True, 'result': doc}), 200)

    else:
        return make_response(jsonify({'success': False, 'message': 'Invalid email or password.'}), 401)


# 400 - Bad request (missing email or password)
# 409 - Conflict (email already exists)
# 201 - Created (user created)
@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()

    if 'email' not in data or 'password' not in data:
        return make_response(jsonify({'success': False, 'message': 'Invalid request.'}), 400)

    email = data['email']
    password = data['password']

    if user_db.Query_One({'email': email}):
        return make_response(jsonify({'success': False, 'message': 'Email already exists.'}), 409)
    
    else:
        user_db.Insert_One({'email': email, 'password': hash_password(password)})
        return make_response(jsonify({'success': True}), 201)