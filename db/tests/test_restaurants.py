import pytest
import db.restaurants as rest

def test_get_nearby_restaurants():
    zip_code = "10004"
    gen_rest = rest.get_nearby_restaurants(zip_code)
    assert isinstance(gen_rest, dict)
    for rest_key in gen_rest:
        assert isinstance(rest_key, str)
        rest_store = gen_rest[rest_key]
        assert isinstance(rest_store, dict)

        assert rest.NAME in rest_store
        assert rest.ADDRESS in rest_store
        assert rest.ZIPCODE in rest_store
        assert rest.OWNER_ID in rest_store
        assert rest.RESTAURANT_ID in rest_store

        assert isinstance(rest_store[rest.NAME], str)
        assert isinstance(rest_store[rest.ADDRESS], str)
        assert isinstance(rest_store[rest.ZIPCODE], str)
        assert isinstance(rest_store[rest.OWNER_ID], int)
        assert isinstance(rest_store[rest.RESTAURANT_ID], int)

        assert gen_rest[rest_key][rest.ZIPCODE] == zip_code


def test_get_restaurants():
    gen_rest = rest.get_restaurants()
    assert isinstance(gen_rest, dict)
    for rest_key in gen_rest:
        assert isinstance(rest_key, str)
        rest_store = gen_rest[rest_key]
        assert isinstance(rest_store, dict)

        assert rest.NAME in rest_store
        assert rest.ADDRESS in rest_store
        assert rest.ZIPCODE in rest_store
        assert rest.OWNER_ID in rest_store
        assert rest.RESTAURANT_ID in rest_store

        assert isinstance(rest_store[rest.NAME], str)
        assert isinstance(rest_store[rest.ADDRESS], str)
        assert isinstance(rest_store[rest.ZIPCODE], str)
        assert isinstance(rest_store[rest.OWNER_ID], int)
        assert isinstance(rest_store[rest.RESTAURANT_ID], int)


def test_add_restaurant():
    store_name = 'Local Seafood'
    store_address = '153 Broadway St'
    store_zipcode = '10004'
    new_restaurant = f'User_{len(rest.get_restaurants())}'
    rest.add_restaurant(store_name, store_address, store_zipcode)
    assert new_restaurant in rest.get_restaurants()


def test_duplicate_restaurant_location():
    store_name = 'Local Seafood'
    store_address = '242 Chicken Street'
    store_zipcode = '10002'
    with pytest.raises(ValueError):
        rest.add_restaurant(store_name, store_address, store_zipcode)


def test_empty_restaurant_input():
    store_name = ''
    store_address = '242 Chicken Street'
    store_zipcode = ''
    with pytest.raises(ValueError):
        rest.add_restaurant(store_name, store_address, store_zipcode)

