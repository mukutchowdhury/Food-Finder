"""
reservations.py: contains reservations made by users
and stored using restaurant_id as key
"""

import db.db_connect as dbc

USERNAME = 'username'
TIME = 'time'
PARTY_SIZE = 'party_size'

RESERVATION_DB = 'reservationdb'
RESTAURANT_NAME = 'restaurant_name'
RESERV_COLLECT = 'reservations'

# reservations can be made by users
reservations = {
    'Terrific Tacos': {
        USERNAME: "Jack",
        TIME: '2023-11-08 19:00',
        PARTY_SIZE: 5
    }
}


def get_all_reservations():
    dbc.connect_db()
    return dbc.fetch_all_as_dict(RESTAURANT_NAME,
                                 RESERV_COLLECT,
                                 RESERVATION_DB)


def get_rest_reservation(restaurant_id):
    if restaurant_id not in reservations:
        raise ValueError("no reservations made for " + restaurant_id)

    return dbc.fetch_one(RESERV_COLLECT, {RESTAURANT_NAME: restaurant_id},
                         RESERVATION_DB)
    # return reservations[restaurant]


def del_reservations(rest_name: str):
    if exists(rest_name):
        return dbc.del_one(RESERV_COLLECT,
                           {RESTAURANT_NAME: rest_name},
                           RESERVATION_DB)


def make_reservation(restaurant, user_name, time, party_size):
    if restaurant not in reservations:
        reservations[restaurant] = []

    reservations[restaurant].append({
        USERNAME: user_name,
        TIME: time,
        PARTY_SIZE: party_size
    })

    dbc.connect_db()
    _id = dbc.insert_one(RESERV_COLLECT, restaurant, RESERVATION_DB)
    return _id is not None


def exists(rest_name: str) -> bool:
    dbc.connect_db()
    return dbc.fetch_one(RESERV_COLLECT, {RESTAURANT_NAME: rest_name},
                         RESERVATION_DB)
