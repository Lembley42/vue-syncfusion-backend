from flask import Flask, request, jsonify
from flask_cors import CORS
import pymongo, json, os, datetime

import routes.auth as auth
import routes.projects as projects
from config import API_KEY

app = Flask(__name__)
CORS(app)

# Register blueprints
for bp in [auth, projects]:
    app.register_blueprint(bp.bp)



# Before request
@app.before_request
def before_request():
    if request.args.get('api_key') != API_KEY:
        return jsonify({'success': False, 'message': 'Invalid API key.'})


if __name__ == '__main__':
    app.run(debug=True)



