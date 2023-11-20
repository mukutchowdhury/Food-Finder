"""
restaurants.py: the interface to our restaurant data.
"""

import random

import db.db_connect as dbc

BIG_NUM = 1_000_000_000

ADDRESS = 'address'
ZIPCODE = 'zipcode'
NAME = 'name'
OWNER_ID = 'owner_id'
RESTAURANT_ID = 'restaurant_id'

REST_NAME = 'rest_name'
REST_ADDRESS = 'rest_address'
REST_ZIPCODE = 'rest_zipcode'

REST_COLLECT = 'restaurants'

# Make a list of all restaruant for all users; for now,
# one restaurant per user
restaurants = {}

def _get_test_address():
    address_text = 'TEST'
    address_nummber = str(random.randint(0, BIG_NUM)) + address_text
    return address_nummber


def _get_test_zipcode():
    min_zip = 10000
    max_zip = 99999
    random_zip = random.randint(min_zip, max_zip)
    return random_zip


def get_test_restaurant():
    test_rest = {}
    test_rest[REST_NAME] = 'TEST_NAME'
    test_rest[REST_ADDRESS] = _get_test_address()
    test_rest[REST_ZIPCODE] = _get_test_zipcode()
    return test_rest


def get_nearby_restaurants(zip_code: str):
    nearby_rest = {}
    for rest_key in restaurants:
        if (restaurants[rest_key][ZIPCODE] == zip_code):
            nearby_rest[rest_key] = restaurants[rest_key]
    return nearby_rest


def add_restaurant(restaurant_id: int, store_name: str,  store_address: str,
                   store_zipcode: str, owner_id: int) -> int:
    for rest_key in restaurants:
        rest = restaurants[rest_key]

        if rest[RESTAURANT_ID] == restaurant_id:
            raise ValueError("restaurant id exists")

        if (rest[ADDRESS] == store_address and
           rest[ZIPCODE] == store_zipcode):
            raise ValueError("Location already has a store")

        if not (store_name and store_address and store_zipcode and owner_id):
            raise ValueError("All attributes must be filled out")

    restaurant = {
        RESTAURANT_ID: restaurant_id,
        NAME: store_name,
        ADDRESS: store_address,
        ZIPCODE: store_zipcode,
        OWNER_ID: owner_id
    }

    dbc.connect_db()
    _id = dbc.insert_one(REST_COLLECT, restaurant)
    return _id is not None


def del_restaurant(restaurant_id: int):
    if exists(restaurant_id):
        return dbc.del_one(REST_COLLECT, {NAME: restaurant_id})
    else:
        raise ValueError(f'Delete failure: {restaurant_id} not in database.')
    

###
def get_restaurants():
    # return restaurants
    dbc.connect_db()
    return dbc.fetch_all_as_dict(RESTAURANT_ID, REST_COLLECT)


def exists(restaurant_id: int) -> bool:
    dbc.connect_db()
    return dbc.fetch_one(REST_COLLECT, {RESTAURANT_ID: restaurant_id})


###