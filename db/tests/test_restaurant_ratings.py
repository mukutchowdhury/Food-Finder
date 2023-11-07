import pytest

import db.ratings as restratings


def test_get_restaurant_ratings():
    ratings = restratings.get_ratings()
    assert isinstance(ratings, dict)
    assert len(ratings) > 0
    for restaurant in ratings:
        assert isinstance(restaurant, str)
        assert isinstance(ratings[restaurant], dict)


def test_add_empty_restaurant():
    with pytest.raises(ValueError):
        restratings.add_restaurant_rating('', 1, 'some review', 5)


NEW_RESTAURANT_NAME = 'Spicy Sandwiches'


def test_add_new_restaurant():
    restratings.add_restaurant_rating(NEW_RESTAURANT_NAME, 4, "Terrible", 1)
    assert NEW_RESTAURANT_NAME in restratings.get_ratings()