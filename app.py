from flask import Flask, request, jsonify
from flask_cors import CORS
import pymongo, json, os, datetime

from routes.auth import auth_bp
from routes.projects import projects_bp
from config import API_KEY

app = Flask(__name__)
CORS(app)

# Register blueprints
for bp in [auth_bp, projects_bp]:
    app.register_blueprint(bp)



# Before request
@app.before_request
def before_request():
    if request.args.get('api_key') != API_KEY:
        return jsonify({'success': False, 'message': 'Invalid API key.'})


if __name__ == '__main__':
    app.run(debug=True)



