"""
restaurants.py: the interface to our restaurant data.
"""

import random
BIG_NUM = 1_000_000_000_000

ADDRESS = 'address'
ZIPCODE = 'zipcode'
NAME = 'name'
OWNER_ID = 'owner_id'
RESTAURANT_ID = 'restaurant_id'

REST_NAME = 'rest_name'
REST_ADDRESS = 'rest_address'
REST_ZIPCODE = 'rest_zipcode'

# Make a list of all restaruant for all users; for now,
# one restaurant per user
restaurants = {
    "User_1": {
        NAME: "Taco Spot",
        ADDRESS: "92 Water Ave",
        ZIPCODE: "10004",
        OWNER_ID: 1,
        RESTAURANT_ID: 1
    },
    "User_2": {
        NAME: "Italian Spot",
        ADDRESS: "242 Chicken Street",
        ZIPCODE: "10002",
        OWNER_ID: 2,
        RESTAURANT_ID: 2
    },
    "User_3": {
        NAME: "Bonjour Spot",
        ADDRESS: "3 Wall Street",
        ZIPCODE: "10004",
        OWNER_ID: 3,
        RESTAURANT_ID: 3
    }
}


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


def get_restaurants():
    return restaurants


def get_nearby_restaurants(zip_code: str):
    nearby_rest = {}
    for rest_key in restaurants:
        if (restaurants[rest_key][ZIPCODE] == zip_code):
            nearby_rest[rest_key] = restaurants[rest_key]
    return nearby_rest


def add_restaurant(store_name: str,  store_address: str, store_zipcode: str):
    for rest_key in restaurants:
        rest = restaurants[rest_key]
        if (rest[ADDRESS] == store_address and
           rest[ZIPCODE] == store_zipcode):
            raise ValueError("Location already has a store")

        if not (store_name and store_address and store_zipcode):
            raise ValueError("All attributes must be filled out")

    new_entry = f'User_{len(restaurants)}'
    restaurants[new_entry] = {
        NAME: store_name,
        ADDRESS: store_address,
        ZIPCODE: store_zipcode,
        OWNER_ID: f'{len(restaurants)}',
        RESTAURANT_ID: f'{len(restaurants)}'
    }
