from flask import Blueprint, request, jsonify, make_response
from services.mongodb import MongoDB
from services.hashing import hash_password, verify_password
from services.utilities import Get_Data

user_db = MongoDB('general', 'users')
auth_bp = Blueprint('auth', __name__, url_prefix='/auth')


# 400 - Bad request (missing email or password)
# 401 - Unauthorized (invalid email or password)
# 200 - OK (user logged in)
@auth_bp.route('/login', methods=['POST'])
def login():
    if data:=Get_Data(request, ['email', 'password']):
        email, password = data
    else: return make_response(jsonify({'message': 'Invalid request.'}), 400)

    result = user_db.Query_One({'email': email})
    if result and verify_password(password, result['password']):
        return make_response(jsonify({'result': str(result['_id'])}), 200)
    else:
        return make_response(jsonify({'message': 'Invalid email or password.'}), 401)


# 400 - Bad request (missing email or password)
# 409 - Conflict (email already exists)
# 201 - Created (user created)
@auth_bp.route('/register', methods=['POST'])
def register():
    if data:=Get_Data(request, ['email', 'password']):
        email, password = data
    else: return make_response(jsonify({'message': 'Invalid request.'}), 400)

    if user_db.Query_One({'email': email}):
        return make_response(jsonify({'message': 'Email already exists.'}), 409)
    
    result = user_db.Insert_One({'email': email, 'password': hash_password(password)})
    return make_response(jsonify({'result': result}), 201)
