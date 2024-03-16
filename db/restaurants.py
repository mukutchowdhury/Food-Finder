"""
restaurants.py: the interface to our restaurant data.
"""

import random

import db.db_connect as dbc

# from openai import OpenAI
# client = OpenAI()


BIG_NUM = 1_000_000_000

OWNER_ID = 'owner_id'
RESTAURANT_ID = 'restaurant_id'

NAME = 'name'
ADDRESS = 'address'
ZIPCODE = 'zipcode'
IMAGE = 'image'
PHONE = 'phone'
CUISINE = 'cuisine'
KEYWORDS = 'keywords'
CATEGORY = 'category'

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


def _get_test_OWNER_ID():
    owner_id = random.randint(0, BIG_NUM)
    return owner_id


def _get_test_rest_id():
    restaurant_id = random.randint(0, BIG_NUM)
    return restaurant_id


def get_test_restaurant():
    test_rest = {}
    test_rest[RESTAURANT_ID] = _get_test_rest_id()
    test_rest[NAME] = 'TEST_NAME'
    test_rest[ADDRESS] = _get_test_address()
    test_rest[ZIPCODE] = _get_test_zipcode()
    test_rest[OWNER_ID] = _get_test_OWNER_ID()
    return test_rest


# GOOD #
def get_restuarant(restaurant_id: int):
    if exists(restaurant_id):
        return dbc.fetch_one(REST_COLLECT, {RESTAURANT_ID: restaurant_id})
    raise ValueError(f'Get failure: {restaurant_id} not found.')


def get_restaurants_by_zipcode(zipcode):
    dbc.connect_db()
    data = dbc.fetch_all_as_dict(RESTAURANT_ID, REST_COLLECT)
    filteredData = {}
    for restaurant in data:
        if (data[restaurant]["zipcode"] == str(zipcode)):
            filteredData[restaurant] = data[restaurant]
    return filteredData


def del_restaurant(restaurant_id: int):
    if exists(restaurant_id):
        return dbc.del_one(REST_COLLECT,
                           {RESTAURANT_ID: restaurant_id})
    raise ValueError(f'Delete failure: {restaurant_id} not found.')


def add_restaurant(data: dict) -> dict:
    restaurant_id = _get_test_rest_id()
    restaurant = {
        RESTAURANT_ID: restaurant_id,
        NAME: data.get('name'),
        ADDRESS: data.get('address'),
        ZIPCODE: data.get('zipcode'),
        OWNER_ID: data.get('owner_id'),
        IMAGE: data.get('image'),
        PHONE: data.get('phone'),
        CUISINE: data.get('cuisine'),
        KEYWORDS: data.get('keywords'),
        CATEGORY: data.get('category')
    }

    dbc.connect_db()
    _id = dbc.insert_one(REST_COLLECT, restaurant)
    return {
        "status": _id is not None,
        "restaurant_id": restaurant_id
    }


def get_restaurants():
    dbc.connect_db()
    return dbc.fetch_all_as_dict(RESTAURANT_ID, REST_COLLECT)


def exists(restaurant_id: int) -> bool:
    dbc.connect_db()
    return dbc.fetch_one(REST_COLLECT, {RESTAURANT_ID: restaurant_id})
