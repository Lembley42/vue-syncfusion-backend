from flask import Blueprint, request, jsonify
from services.mongodb import MongoDB
from services.jsonencode import Get_Encoder
import bson, json

project_db = MongoDB('general', 'projects')
projects_bp = Blueprint('projects', __name__, url_prefix='/projects')


@projects_bp.route('/create', methods=['POST'])
def create():
    data = request.get_json()
    project_db.Insert_One(data)
    return jsonify({'success': True}), 200
    


@projects_bp.route('/get/byProjectId/<string:project_id>', methods=['GET'])
def get_byprojectid(project_id):
    result = project_db.Query_One({'_id': bson.ObjectId(project_id)})
    json_data = json.dumps(result, cls=Get_Encoder())
    return json_data, 200


@projects_bp.route('/get/byUserId/<string:user_id>', methods=['GET'])
def get_byuserid(user_id):
    results = project_db.Query({ 'user_ids': { '$in': [user_id] } })
    json_data = json.dumps(list(results), cls=Get_Encoder())
    return json_data, 200


@projects_bp.route('/update/byProjectId/<string:project_id>', methods=['POST'])
def update_byprojectid(project_id):
    data = request.get_json()
    project_db.Update_One({'_id': bson.ObjectId(project_id)}, {'$set': data})
    return jsonify({'success': True}), 200


@projects_bp.route('/delete/byProjectId/<string:project_id>', methods=['POST'])
def delete_byproject(project_id):
    project_db.Delete_One({'_id': bson.ObjectId(project_id)})
    return jsonify({'success': True}), 200


