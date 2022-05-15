import requests
from utils import range_date

BASE_URL = "https://test.api.amadeus.com"
DATA_URL = "https://test.api.amadeus.com"


def api_get_token(client_id: str, client_secret: str):
    url = "{}/v1/security/oauth2/token".format(BASE_URL)
    data = {"grant_type": 'client_credentials', "client_id": client_id,
            "client_secret": client_secret}
    result = requests.post(url, data=data).json()
    return result["access_token"]


def api_get_one_flight_details(user_token: str, values):
    url = "{}/v2/shopping/flight-offers".format(DATA_URL)
    headers = {"content-type": "application/json; charset=UTF-8", 'Authorization': 'Bearer {}'.format(user_token)}
    result = requests.get(url, params=values, headers=headers).json()
    return result


def api_get_all_fligths(user_token:str, destination, arrival, start_date, end_date, max_adults, max_children):
    for departure_date in range_date(start_date, end_date):
        for nb_adults in range(1, max_adults+1):
            for nb_children in range(max_children+1):
                values = {"originLocationCode": destination, "destinationLocationCode": arrival,
                          "departureDate": departure_date, "adults": nb_adults, "children": nb_children}
                url = "{}/v2/shopping/flight-offers".format(DATA_URL)
                headers = {"content-type": "application/json; charset=UTF-8",
                           'Authorization': 'Bearer {}'.format(user_token)}
                result = requests.get(url, params=values, headers=headers).json()
                yield result, nb_adults, nb_children
