import pytest

import db.ratings as restnts


def test_get_restaurant_ratings():
    restaurants = restnts.get_ratings()
    assert isinstance(restaurants, dict)
    assert len(restaurants) > 0
    for restaurant in restaurants:
        assert isinstance(restaurant, str)
        assert isinstance(restaurants[restaurant], dict)
    assert restnts.TEST_RESTAURANT_NAME in restaurants


def test_add_copy_restaurant():
    with pytest.raises(ValueError):
        restnts.add_restaurant_rating(restnts.TEST_RESTAURANT_NAME, "Terrible")


def test_add_empty_restaurant():
    with pytest.raises(ValueError):
        restnts.add_restaurant_rating('', "Terrible")


NEW_RESTAURANT_NAME = 'Spicy Sandwiches'


def test_add_new_restaurant():
    restnts.add_restaurant_rating(NEW_RESTAURANT_NAME, "Terrible")
    assert NEW_RESTAURANT_NAME in restnts.get_ratings()