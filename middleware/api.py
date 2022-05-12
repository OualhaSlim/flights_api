import requests

BASE_URL = "https://test.api.amadeus.com"
DATA_URL = "https://test.api.amadeus.com"


def api_get_token(client_id: str, client_secret: str):
    url = "{}/v1/security/oauth2/token".format(BASE_URL)
    data = {"grant_type": 'client_credentials', "client_id": client_id,
            "client_secret": client_secret}
    result = requests.post(url, data=data).json()
    print(result)
    return result["access_token"]

def api_get_all_data(user_token: str, values):
    url = "{}/v2/shopping/flight-offers".format(DATA_URL)

    headers = {"content-type": "application/json; charset=UTF-8", 'Authorization': 'Bearer {}'.format(user_token)}
    result = requests.get(url, params=values, headers=headers).json()
    return result
