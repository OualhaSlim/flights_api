from pymongo import MongoClient

client = MongoClient()
DB = client["flights-api-db"]


def add_flight_to_db(result, nb_adults, nb_children):
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

        elif (len(flight_details["segments"]) > 1):
            departure_details = flight_details["segments"][0]["departure"]
            departure_city_code = departure_details["iataCode"]
            departure_date = departure_details["at"]

            arrival_details = flight_details["segments"][-1]["arrival"]
            arrival_city_code = arrival_details["iataCode"]
            arrival_date = arrival_details["at"]

            all_intermediate_flights = []
            for intermediate_flight in flight_details["segments"][1:]:
                intermediate_flight_details = intermediate_flight["departure"]
                intermediate_city_code = intermediate_flight_details["iataCode"]
                all_intermediate_flights.append(intermediate_city_code)

            new_flight_details = {"lieu_depart": departure_city_code, "lieu_arrivee": arrival_city_code,
                                  "date_depart": departure_date, "date_arrivee": arrival_date, "prix": total_price,
                                  "remaining_places": remaining_places, "durée": total_duration, "stop": True,
                                  "vol_intermediaire": all_intermediate_flights}
        new_flight_details["nombre_adultes"] = nb_adults
        new_flight_details["nombre_enfants"] = nb_children
        flights_collection.insert_one(new_flight_details)


def remove_all_data():
    flights_collection = DB["flights"]
    response = flights_collection.delete_many({})
    return response.deleted_count
