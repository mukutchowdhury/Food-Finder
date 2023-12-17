"""
restaurants.py: the interface to our restaurant data.
"""

import random

import db.db_connect as dbc

# from openai import OpenAI
# client = OpenAI()


BIG_NUM = 1_000_000_000

ADDRESS = 'address'
ZIPCODE = 'zipcode'
NAME = 'name'

OWNER_ID = 'rest_owner_id'
RESTAURANT_ID = 'restaurant_id'

REST_NAME = 'rest_name'
REST_ADDRESS = 'rest_address'
REST_ZIPCODE = 'rest_zipcode'

REST_COLLECT = 'restaurants'

# Make a list of all restaruant for all users; for now,
# one restaurant per user
restaurants = {}


def _get_test_name():
    name = 'test'
    rand_part = random.randint(0, BIG_NUM)
    return name + str(rand_part)


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


def get_test_restaurant():
    test_rest = {}
    test_rest[NAME] = _get_test_name()
    test_rest[ADDRESS] = _get_test_address()
    test_rest[ZIPCODE] = _get_test_zipcode()
    test_rest[OWNER_ID] = _get_test_OWNER_ID()
    return test_rest


def get_nearby_restaurants(zip_code: str):
    # completion = client.chat.completions.create(
    #     model="gpt-3.5-turbo",
    #     messages=[
    #         {"role": "system", "content": "You provide nearby zipcode" +
    #          "using the zipcode the user provides as reference"},
    #         {"role": "user", "content": f'{zip_code}'}
    #     ]
    # )
    # return completion.choices[0].message
    pass


# GOOD #
def get_restuarant(restaurant_id: int):
    if exists(restaurant_id):
        return dbc.fetch_one(REST_COLLECT, {RESTAURANT_ID: restaurant_id})
    raise ValueError(f'Get failure: {restaurant_id} not found.')


def del_restaurant(restaurant_id: int):
    if exists(restaurant_id):
        return dbc.del_one(REST_COLLECT,
                           {RESTAURANT_ID: restaurant_id})
    raise ValueError(f'Delete failure: {restaurant_id} not found.')


def add_restaurant(store_name: str,  store_address: str,
                   store_zipcode: str, owner_id: int) -> dict:

    if not (store_name and store_address and store_zipcode and owner_id):
        raise ValueError("All attributes must be filled out")

    restaurant_id = random.randint(0, BIG_NUM)
    while exists(restaurant_id):
        restaurant_id = random.randint(0, BIG_NUM)

    restaurant = {
        RESTAURANT_ID: restaurant_id,
        NAME: store_name,
        ADDRESS: store_address,
        ZIPCODE: store_zipcode,
        OWNER_ID: owner_id
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
