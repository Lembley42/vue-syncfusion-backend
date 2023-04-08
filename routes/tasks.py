from flask import Blueprint, request, jsonify, make_response
from services.mongodb import MongoDB
from services.jsonencode import Get_Encoder
from services.utilities import Get_Data
import bson, json

tasks_db = MongoDB('general', 'tasks')
tasks_bp = Blueprint('tasks', __name__, url_prefix='/tasks')


# 400 - Bad request (missing project_id or name)
# 201 - Created (task created)
@tasks_bp.route('/create', methods=['POST'])
def create():
    if data := Get_Data(request, ['project_id', 'name']):
        project_id, name = data
    else: return make_response(jsonify({'message': 'Invalid request.'}), 400)

    tasks_db.Insert_One({'project_id': project_id, 'name': name})
    return make_response(jsonify({'success': True}), 201)


# 404 - Not found (task not found)
# 200 - OK (task found)
@tasks_bp.route('/get/byProjectId/<string:project_id>', methods=['GET'])
def get_byprojectid(project_id):
    result = tasks_db.Query({ 'project_id': project_id })

    if not result:
        return make_response(jsonify({'success': False, 'message': 'No tasks found.'}), 404)
    
    json_data = json.dumps(list(result), cls=Get_Encoder())
    return make_response({'success': True, 'result': json_data}, 200)


# 404 - Not found (task not found)
# 200 - OK (task found)
@tasks_bp.route('/get/byTaskId/<string:task_id>', methods=['GET'])
def get_bytaskid(task_id):
    result = tasks_db.Query_One({'_id': bson.ObjectId(task_id)})

    if not result:
        return make_response(jsonify({'success': False, 'message': 'Task not found.'}), 404)

    json_data = json.dumps(result, cls=Get_Encoder())
    return make_response({'success': True, 'result': json_data}, 200)


# 400 - Bad request (missing name)
# 200 - OK (task updated)
@tasks_bp.route('/update/byTaskId/<string:task_id>', methods=['POST'])
def update_bytaskid(task_id):
    if data:= Get_Data(request, ['name']):
        name = data
    else: return make_response(jsonify({'message': 'Invalid request.'}), 400)

    tasks_db.Update_One({'_id': bson.ObjectId(task_id)}, {'$set': {'name': name}})
    return make_response(jsonify({'success': True}), 200)



# 200 - OK (task deleted)
@tasks_bp.route('/delete/byTaskId/<string:task_id>', methods=['POST'])
def delete_bytaskid(task_id):
    tasks_db.Delete_One({'_id': bson.ObjectId(task_id)})
    return make_response(jsonify({'success': True}), 200)


