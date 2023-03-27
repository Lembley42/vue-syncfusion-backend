from flask import Blueprint, request, jsonify
from services.mongodb import MongoDB
import bson

project_db = MongoDB('general', 'projects')
projects = Blueprint('auth', __name__, url_prefix='/projects')


@projects.route('/create', methods=['POST'])
def create():
    data = request.get_json()
    project_db.Insert_One(data)
    return jsonify({'success': True})


@projects.route('/get/byProjectId/{project_id}', methods=['GET'])
def get(project_id):
    project_db.Query_One({'_id': bson.ObjectId(project_id)})


@projects.route('/get/byUserId/{user_id}', methods=['GET'])
def get(user_id):
    results = project_db.Query({ 'user_ids': { '$in': [user_id] } })
    return jsonify({'success': True, 'results': results})


@projects.route('/update/byProjectId/{project_id}', methods=['POST'])
def update(project_id):
    data = request.get_json()
    project_db.Update_One({'_id': bson.ObjectId(project_id)}, {'$set': data})
    return jsonify({'success': True})


@projects.route('/delete', methods=['POST'])
def delete():
    data = request.get_json()
    id = data['_id']
    project_db.Delete_One({'_id': bson.ObjectId(id)})
    return jsonify({'success': True})


