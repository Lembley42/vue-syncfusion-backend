from flask import Blueprint, request, jsonify, make_response
from services.mongodb import MongoDB
from services.jsonencode import Get_Encoder
import bson, json

project_db = MongoDB('general', 'projects')
projects_bp = Blueprint('projects', __name__, url_prefix='/projects')



# 400 - Bad request (missing name or user_ids)
# 201 - Created (project created)
@projects_bp.route('/create', methods=['POST'])
def create():
    data = request.get_json()

    if 'name' not in data or 'user_ids' not in data:
        return make_response(jsonify({'success': False, 'message': 'Invalid request.'}), 400)
    
    project_db.Insert_One(data)
    return make_response(jsonify({'success': True}), 201)


# 404 - Not found (project not found)
# 200 - OK (project found)
@projects_bp.route('/get/byProjectId/<string:project_id>', methods=['GET'])
def get_byprojectid(project_id):
    result = project_db.Query_One({'_id': bson.ObjectId(project_id)})
    
    if not result:
        return make_response(jsonify({'success': False, 'message': 'Project not found.'}), 404)

    json_data = json.dumps(result, cls=Get_Encoder())
    return make_response({'success': True, 'result': json_data}, 200)


# 404 - Not found (no projects found)
# 200 - OK (projects found)
@projects_bp.route('/get/byUserId/<string:user_id>', methods=['GET'])
def get_byuserid(user_id):
    results = project_db.Query({ 'user_ids': { '$in': [user_id] } })

    if not results:
        return make_response(jsonify({'success': False, 'message': 'No projects found.'}), 404)

    json_data = json.dumps(list(results), cls=Get_Encoder())
    return make_response({'success': True, 'result': json_data}, 200)


# 400 - Bad request (missing name or user_ids)
# 200 - OK (project updated)
@projects_bp.route('/update/byProjectId/<string:project_id>', methods=['POST'])
def update_byprojectid(project_id):
    data = request.get_json()

    if 'name' not in data or 'user_ids' not in data:
        return make_response(jsonify({'success': False, 'message': 'Invalid request.'}), 400)

    project_db.Update_One({'_id': bson.ObjectId(project_id)}, {'$set': data})
    return make_response(jsonify({'success': True}), 200)


# 200 - OK (project deleted)
@projects_bp.route('/delete/byProjectId/<string:project_id>', methods=['POST'])
def delete_byproject(project_id):
    project_db.Delete_One({'_id': bson.ObjectId(project_id)})
    return make_response(jsonify({'success': True}), 200)


