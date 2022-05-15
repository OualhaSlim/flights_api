from flask import Flask, request
import json
import itertools
from middleware.api import api_get_token, api_get_one_flight_details, api_get_all_fligths
from db import add_flight_to_db, remove_all_data, get_flights_by_dep_and_arr

airports_file = open('airports.json')
airports = json.load(airports_file)

app = Flask(__name__)
# app.config["MONGO_URI"] = "mongodb://localhost:27017/flights-api"
# mongodb_client = PyMongo(app, uri="mongodb://localhost:27017/flights-api")


@app.route('/api/get_token', methods=['POST'])
def get_token():
    data = request.get_json()
    client_id, client_secret = data['client_id'], data['client_secret']
    result = api_get_token(client_id, client_secret)
    return result


@app.route('/api/get_flight')
def get_one_flight_details_api():
    access_token = request.headers['access_token']
    result = api_get_one_flight_details(access_token, request.form)
    if 'data' not in result:
        return result['errors'][0]['detail']
    nb_adults = int(request.form['adults'])
    nb_children = 0
    if 'children' in request.form:
        nb_children = int(request.form['children'])
    add_flight_to_db(result["data"], nb_adults, nb_children)
    return result


@app.route('/api/update_db')
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
    start_date = request.form['startDate']
    end_date = request.form['endDate']
    max_adults = int(request.form['maxAdults'])
    max_children = int(request.form['maxChildren'])
    for dep, arr in all_codes_combinations:
        for result, nb_adults, nb_children in api_get_all_fligths(access_token, dep, arr,
                                                                  start_date, end_date, max_adults, max_children):
            if 'data' not in result:
                if result['errors'][0]['detail'] == "The access token is expired":
                    return result['errors'][0]['detail']
                print(result['errors'][0]['detail'])
                continue
            add_flight_to_db(result["data"], nb_adults, nb_children)
    return "done"


@app.route('/empty_db', methods=['POST'])
def remove_all():
    removed_count = remove_all_data()
    return "delete success {}".format(removed_count)


@app.route('/get_flight')
def get_one_flight_details():
    result = get_flights_by_dep_and_arr(request.form)
    return result


@app.errorhandler(404)
def page_not_found(e):
    return "page not found"


if __name__ == "__main__":
    app.run(debug=False)

