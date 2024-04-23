import random
import db.db_connect as dbc

ID_LEN = 24
BIG_NUM = 100_000_000_000_000_000_000

MOCK_ID = '0' * ID_LEN

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
HOURS = 'hours'
OPEN = 'open'
CLOSE = 'close'

STATUS = 'status'

# SCHEMA
# {
#     "name": fields.String,
#     "address": fields.String,
#     "zipcode": fields.String,
#     "owner_id": fields.Integer,
#     "image": fields.String,
#     "phone": fields.String,
#     "cuisine": fields.List(fields.String),
#     "keywords": fields.List(fields.String),
#     "category": fields.List(fields.String)
#     "hours": {
#          open: fields.String,
#          close: fields.String,
#      },
# }


def exists(restaurant_id: str) -> bool:
    dbc.connect_db()
    return dbc.fetch_one(REST_COLLECT, {RESTAURANT_ID: restaurant_id})


def _get_test_rest_id() -> str:
    _id = random.randint(0, BIG_NUM)
    _id = str(_id)
    _id = _id.rjust(ID_LEN, '0')
    return _id


def get_test_restaurant():
    test_restaurant = {}
    test_restaurant[NAME] = 'TEST'
    test_restaurant[ADDRESS] = 'TEST'
    test_restaurant[ZIPCODE] = '10001'
    test_restaurant[OWNER_ID] = 'TEST'
    test_restaurant[IMAGE] = 'TEST'
    test_restaurant[PHONE] = '10001'
    test_restaurant[CUISINE] = []
    test_restaurant[KEYWORDS] = []
    test_restaurant[CATEGORY] = []
    test_restaurant[HOURS] = {
        OPEN: 'TEST',
        CLOSE: 'TEST'
    }
    return test_restaurant


def get_test_add_return():
    test_return = {}
    test_return[STATUS] = True
    test_return[RESTAURANT_ID] = MOCK_ID
    return test_return


def get_test_bad_add_return():
    test_return = {}
    test_return[STATUS] = None
    test_return[RESTAURANT_ID] = MOCK_ID
    return test_return


def get_test_update_hour():
    return {OPEN: 'TEST', CLOSE: 'TEST'}


def get_restaurant(restaurant_id: str):
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


def del_restaurant(restaurant_id: str):
    if exists(restaurant_id):
        return dbc.del_one(REST_COLLECT,
                           {RESTAURANT_ID: restaurant_id})
    raise ValueError(f'Delete failure: {restaurant_id} not found.')


def add_restaurant(data: dict) -> dict:
    if (not (data.get('name') and data.get('address')
       and data.get('zipcode') and data.get('owner_id'))):
        raise ValueError('Values have not been filled in!')
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
        CATEGORY: data.get('category'),
        HOURS: data.get('hours')
    }
    dbc.connect_db()

    _id = dbc.insert_one(REST_COLLECT, restaurant)
    return {
        "status": _id is not None,
        "restaurant_id": restaurant_id
    }


def get_all_restaurants():
    dbc.connect_db()
    return dbc.fetch_all_as_dict(RESTAURANT_ID, REST_COLLECT)


# Hours Operations
def update_restaurant_time(restaurant_id: str,
                           open: str, close: str):
    if exists(restaurant_id):
        return dbc.up_one(REST_COLLECT, {RESTAURANT_ID: restaurant_id},
                          {"$set": {HOURS: {OPEN: open, CLOSE: close}}})
    raise ValueError('PUT failure: ' +
                     f'{restaurant_id} has no existing time')
