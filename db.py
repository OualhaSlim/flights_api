from pymongo import MongoClient

client = MongoClient()
DB = client["flights-api-db"]


def add_flight_to_db(result):
    flights_collection = DB["flights"]
    for flight in result:
        remaining_places = flight["numberOfBookableSeats"]
        total_price = flight["price"]["total"]
        flight_details = flight["itineraries"][0]
        total_duration = flight_details["duration"]
        # in case direct flight
        if (len(flight_details["segments"]) == 1):  # ---CAS 1----#  #C pas possible combien de for #id pour plusieurs requetes
            departure_details = flight_details["segments"][0]["departure"]
            departure_city_code = departure_details["iataCode"]
            departure_date = departure_details["at"]

            arrival_details = flight_details["segments"][0]["arrival"]
            arrival_city_code = arrival_details["iataCode"]
            arrival_date = arrival_details["at"]

            new_flight_details = {"lieu_depart": departure_city_code, "lieu_arrivee": arrival_city_code,
                     "date_depart": departure_date, "date_arrivee": arrival_date, "prix": total_price,
                     "remaining_places": remaining_places, "durée": total_duration}
            flights_collection.insert_one(new_flight_details)
        # elif (len(flight_details["segments"]) > 1):
        #     compteur = 0
        #     v_comp = ""
        #     for d in flight_details["segments"]:
        #         a = d["departure"]
        #         lieu_depart = a["iataCode"]
        #         date_depart = a["at"]
        #         e = d["arrival"]
        #         lieu_arrivee = e["iataCode"]
        #         date_arrivee = e["at"]
        #         duree_vol_i = d["duration"]
        #         compteur = compteur + 1
        #         sous_vol_n = {"lieu_depart": lieu_depart, "lieu_arrivee": lieu_arrivee,
        #                       "date_depart": date_depart, "date_arrivee": date_arrivee, "price": total_price,
        #                       "code_escale": 0, "remaining_places": remaining_places, "durée": total_duration}
        #         flights_collection.insert_one(sous_vol_n)


def remove_all_data():
    flights_collection = DB["flights"]
    response = flights_collection.delete_many({})
    return response.deleted_count