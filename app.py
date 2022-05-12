from flask import Flask, request
from flask_pymongo import PyMongo
from middleware.api import api_get_token, api_get_all_data

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/flights-api"
mongo = PyMongo(app)

@app.route('/')
def hello_world():
    return 'This is my first API call!'

@app.route('/get_token', methods=['POST'])
def get_token():
    data = request.get_json()
    client_id, client_secret = data['client_id'], data['client_secret']
    result = api_get_token(client_id, client_secret)
    return result

@app.route('/get_all_data', methods=['GET'])
def get_api_data():
    # print(request.form)
    # return 'hello'
    access_token = request.headers['access_token']
    result = api_get_all_data(access_token, request.form)
    return result

