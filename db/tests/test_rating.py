import pytest

import db.ratings as ratings
import db.restaurants as rest


TEST_RESTAURANT = {
    rest.NAME: 'TEST',
    rest.ADDRESS: 'TEST',
    rest.ZIPCODE: 'TEST',
    rest.OWNER_ID: 1,
    rest.IMAGE: '',
    rest.PHONE: 'TEST',
    rest.CUISINE: [],
    rest.KEYWORDS: [],
    rest.CATEGORY: []
}

REVIEW_ID = 'review_id'
RESTAURANT_ID = 'restaurant_id'
TEXT = 'TEST'
TEST_USER_ID = 1
STAR = 5

@pytest.fixture(scope='function')
def temp_review():
    restaurantid = rest.add_restaurant(TEST_RESTAURANT)[RESTAURANT_ID]
    reviewid = ratings.add_restaurant_rating(restaurantid, TEST_USER_ID, TEXT, STAR )
    yield restaurantid, reviewid[REVIEW_ID]
    if ratings.restaurant_exists(restaurantid):
        rest.del_restaurant(restaurantid)
    if ratings.review_exists(reviewid):
        ratings.del_rating(reviewid)


def test_gen_reviewId():
    _id = ratings._gen_reviewId()
    assert isinstance(_id, str)
    assert len(_id) == ratings.ID_LEN


def test_get_restaurant_ratings(temp_review): 
    restaurantid, reviewid = temp_review
    reviews = ratings.get_restaurant_ratings(restaurantid)
    assert isinstance(reviews, list)
    for review in reviews:
        assert isinstance(review, dict)
    assert ratings.review_exists(reviewid)
    assert ratings.restaurant_exists(restaurantid)


def test_get_restaurant_ratings_NotFound():
    with pytest.raises(ValueError):
        ratings.get_restaurant_ratings(0)


def test_add_restaurant_rating(temp_review):
    restaurantid, _reviewid = temp_review
    ret = ratings.add_restaurant_rating(restaurantid, TEST_USER_ID, TEXT, STAR)
    assert isinstance(ret, dict)
    assert ratings.review_exists(ret[ratings.REVIEW_ID])


def test_add_restaurant_rating_Blank(temp_review):
    restaurantid, _reviewid = temp_review
    with pytest.raises(ValueError):
        ratings.add_restaurant_rating(restaurantid, '', '', 0)


def test_add_restaurant_rating_NotFound():
    with pytest.raises(ValueError):
        ratings.add_restaurant_rating(1, TEST_USER_ID, TEXT, STAR )


def test_update_review_text(temp_review): 
    _restaurantid, reviewid = temp_review
    ratings.update_review_text(reviewid, 'NEW_TEXT')
    assert ratings.review_exists(reviewid)


def test_update_review_text_NotFound():
    with pytest.raises(ValueError):
        ratings.update_review_text(0, '')


def test_del_rating(temp_review):
    _restaurantid, reviewid = temp_review
    ratings.del_rating(reviewid)
    assert not ratings.review_exists(reviewid)


def test_del_rating_NotFound():
    with pytest.raises(ValueError):
        ratings.del_rating(0)
