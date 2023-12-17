import pytest

from db.restaurants import (
    NAME,
    ADDRESS,
    ZIPCODE,
    OWNER_ID,
    RESTAURANT_ID)

import db.restaurants as rest


@pytest.fixture(scope='function')
def test_data():
    test_restaurant = rest.get_test_restaurant()
    added_restaurant = rest.add_restaurant(
        test_restaurant[NAME],
        test_restaurant[ADDRESS],
        test_restaurant[ZIPCODE],
        test_restaurant[OWNER_ID]
    )
    yield added_restaurant

    if rest.exists(added_restaurant["restaurant_id"]):
        rest.del_restaurant(added_restaurant["restaurant_id"])


def test_get_restaurants(test_data):
    added_restaurant_id = test_data["restaurant_id"]
    restaurants = rest.get_restaurants()
    assert added_restaurant_id in restaurants


# def test_get_restaurant(test_data):
#     temp_restaurant_id = test_data["restaurant_id"]
#     temp_rest = rest.get_restuarant(temp_restaurant_id)
#     assert isinstance(temp_rest, dict)

#     if temp_rest is not None:
#         assert temp_rest.get(NAME) == test_restaurant[NAME]
#         assert temp_rest.get('address') == test_restaurant[ADDRESS]
#         assert temp_rest.get('zipcode') == test_restaurant[ZIPCODE]
#         assert temp_rest.get('rest_owner_id') == test_restaurant[OWNER_ID]


# def test_get_nearby_restaurants():
#     zip_code = "10004"
#     gen_rest = rest.get_nearby_restaurants(zip_code)
#     assert isinstance(gen_rest, dict)
#     for rest_key in gen_rest:
#         assert isinstance(rest_key, int)
#         rest_store = gen_rest[rest_key]
#         assert isinstance(rest_store, dict)

#         assert rest.NAME in rest_store
#         assert rest.ADDRESS in rest_store
#         assert rest.ZIPCODE in rest_store
#         assert rest.OWNER_ID in rest_store

#         assert isinstance(rest_store[rest.NAME], str)
#         assert isinstance(rest_store[rest.ADDRESS], str)
#         assert isinstance(rest_store[rest.ZIPCODE], str)
#         assert isinstance(rest_store[rest.OWNER_ID], int)

#         assert gen_rest[rest_key][rest.ZIPCODE] == zip_code


# def test_get_restaurants():
#     gen_rest = rest.get_restaurants()
#     assert isinstance(gen_rest, dict)
#     for rest_key in gen_rest:
#         assert isinstance(rest_key, int)
#         rest_store = gen_rest[rest_key]
#         assert isinstance(rest_store, dict)

#         assert rest.NAME in rest_store
#         assert rest.ADDRESS in rest_store
#         assert rest.ZIPCODE in rest_store
#         assert rest.OWNER_ID in rest_store

#         assert isinstance(rest_store[rest.NAME], str)
#         assert isinstance(rest_store[rest.ADDRESS], str)
#         assert isinstance(rest_store[rest.ZIPCODE], str)
#         assert isinstance(rest_store[rest.OWNER_ID], int)


# def test_add_restaurant():
#     store_name = 'TEST'
#     store_address = 'TEST'
#     store_zipcode = '10004'
#     owner_id = 42
#     rest_id = rest.add_restaurant(store_name, store_address, store_zipcode, owner_id)
#     assert rest_id in rest.get_restaurants()


# def test_duplicate_restaurant_location():
#     store_name = 'TEST'
#     store_address = '242 Chicken Street'
#     store_zipcode = '10002'
#     owner_id = 42
#     with pytest.raises(ValueError):
#         rest.add_restaurant(store_name, store_address, store_zipcode, owner_id)


# def test_empty_restaurant_input():
#     store_name = ''
#     store_address = ''
#     store_zipcode = ''
#     owner_id = 0
#     with pytest.raises(ValueError):
#         rest.add_restaurant(store_name, store_address, store_zipcode, owner_id)


# def test_generate_restaurant_id():
#     rest_id = rest._generate_restaurant_id()
#     assert isinstance(rest_id, int)


# def test_get_test_restaurant():
#     test_rest = rest.get_test_restaurant()
#     assert isinstance(test_rest, dict)


# def test_get_test_address():
#     address = rest._get_test_address()
#     assert isinstance(address, str)


# def test_get_test_zipcode():
#     zipcode = rest._get_test_zipcode()
#     assert isinstance(zipcode, int)