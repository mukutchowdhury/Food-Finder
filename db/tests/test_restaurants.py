import pytest

import db.restaurants as restnts


def test_get_restaurants():
    restaurants = restnts.get_restaurants()
    assert isinstance(restaurants, dict)
    assert len(restaurants) > 0
    for restaurant in restaurants:
        assert isinstance(restaurant, str)
        assert isinstance(restaurants[restaurant], dict)
    assert restnts.TEST_RESTAURANT_NAME in restaurants


def test_add_copy_restaurant():
    with pytest.raises(ValueError):
        restnts.add_restaurant(restnts.TEST_RESTAURANT_NAME, "111 Apple Road")


def test_add_empty_restaurant():
    with pytest.raises(ValueError):
        restnts.add_restaurant('', "111 Apple Road")


NEW_RESTAURANT_NAME = 'Spicy Sandwiches'


def test_add_new_restaurant():
    restnts.add_restaurant(NEW_RESTAURANT_NAME, "111 Cool Street")
    assert NEW_RESTAURANT_NAME in restnts.get_restaurants()