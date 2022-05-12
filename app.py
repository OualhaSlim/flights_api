from flask import Flask, request
import json
import itertools
from middleware.api import api_get_token, api_get_one_flight_details
from db import add_flight_to_db, remove_all_data

airports_file = open('airports.json')
airports = json.load(airports_file)

app = Flask(__name__)
# app.config["MONGO_URI"] = "mongodb://localhost:27017/flights-api"
# mongodb_client = PyMongo(app, uri="mongodb://localhost:27017/flights-api")

@app.route('/')
def hello_world():
    return 'This is my first API call!'

@app.route('/get_token', methods=['POST'])
def get_token():
    data = request.get_json()
    client_id, client_secret = data['client_id'], data['client_secret']
    result = api_get_token(client_id, client_secret)
    return result

@app.route('/empty_db', methods=['POST'])
def remove_all():
    removed_count = remove_all_data()
    return "delete success {}".format(removed_count)


@app.route('/get_flight')
def get_one_flight_details():
    access_token = request.headers['access_token']
    result = api_get_one_flight_details(access_token, request.form)
    if 'data' not in result:
        return result['errors'][0]['detail']
    add_flight_to_db(result["data"])
    return result

@app.route('/update_db')
def update_db():
    access_token = request.headers['access_token']
    all_codes = []
    for airport_details in airports:
        all_codes.append(airport_details["code"])
    all_codes_combinations = []
    for i in range(len(all_codes)-1):
        for j in range(i+1, len(all_codes)):
            all_codes_combinations.append((all_codes[i], all_codes[j]))
            all_codes_combinations.append((all_codes[j], all_codes[i]))
    for dest, arr in all_codes_combinations:
        values = {"originLocationCode": dest, "destinationLocationCode": arr, "departureDate": '2022-05-15',
                  'adults': 1}
        result = api_get_one_flight_details(access_token, values)
        if 'data' not in result:
            continue
        add_flight_to_db(result["data"])

    print(all_codes_combinations)
    return "done"


if __name__ == "__main__":
    app.run(debug=True)

