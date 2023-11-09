import pytest

import db.ratings as restratings

@pytest.fixture(scope='function')
def temp_rating():
    name = restratings._get_test_name()
    ret = restratings.add_restaurant_rating(name, 9787, 'good', 4)
    return name

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

def test_add_dup_restaurant_rating(temp_rating):
    dup_name = temp_rating
    with pytest.raises(ValueError):
        restratings.add_restaurant_rating(dup_name, 1, 'some review', 5)

NEW_RESTAURANT_NAME = 'Spicy Sandwiches'


def test_add_new_restaurant():
    restratings.add_restaurant_rating(NEW_RESTAURANT_NAME, 4, "Terrible", 1)
    assert NEW_RESTAURANT_NAME in restratings.get_ratings()