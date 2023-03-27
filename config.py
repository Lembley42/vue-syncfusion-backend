import os


### MONGO ###
MONGO_URI = os.environ.get('MONGO_URI')
MONGO_USERNAME = os.environ.get('MONGO_USERNAME')
MONGO_PASSWORD = os.environ.get('MONGO_PASSWORD')
MONGO_FULL_URI = f'mongodb+srv://{MONGO_USERNAME}:{MONGO_PASSWORD}@{MONGO_URI}'


### API KEY ###
API_KEY = os.environ.get('API_KEY')