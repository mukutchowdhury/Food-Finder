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
    test_rest = rest.get_test_restaurant()
    added_restaurant = rest.add_restaurant(
        test_rest[RESTAURANT_ID],
        test_rest[NAME],
        test_rest[ADDRESS],
        test_rest[ZIPCODE],
        test_rest[OWNER_ID]
    )
    yield test_rest

    if test_rest:
        rest.del_restaurant(test_rest[RESTAURANT_ID])


def test_add_rest():
    new_rest = rest.get_test_restaurant()
    ret = rest.add_restaurant(new_rest[RESTAURANT_ID],
                              new_rest[NAME],
                              new_rest[ADDRESS],
                              new_rest[ZIPCODE],
                              new_rest[OWNER_ID])
    assert rest.exists(new_rest[RESTAURANT_ID])
    rest.del_restaurant(new_rest[RESTAURANT_ID])


def test_del_rest(test_data):
    del_id = test_data[RESTAURANT_ID]
    # rest.del_restaurant(del_id)
    # assert not rest.exists(del_id)


def test_get_restaurants():
    gen_rest = rest.get_restaurants()
    assert isinstance(gen_rest, dict)
    for rest_key in gen_rest:
        assert isinstance(rest_key, int)
        rest_store = gen_rest[rest_key]
        assert isinstance(rest_store, dict)

        assert rest.NAME in rest_store
        assert rest.ADDRESS in rest_store
        assert rest.ZIPCODE in rest_store
        assert rest.OWNER_ID in rest_store

        assert isinstance(rest_store[rest.NAME], str)
        assert isinstance(rest_store[rest.ADDRESS], str)
        assert isinstance(rest_store[rest.ZIPCODE], str)
        assert isinstance(rest_store[rest.OWNER_ID], int)


def test_generate_restaurant_id():
    rest_id = rest._get_test_rest_id()
    assert isinstance(rest_id, int)


def test_get_test_restaurant():
    test_rest = rest.get_test_restaurant()
    assert isinstance(test_rest, dict)


def test_get_test_address():
    address = rest._get_test_address()
    assert isinstance(address, str)


def test_get_test_zipcode():
    zipcode = rest._get_test_zipcode()
    assert isinstance(zipcode, int)
