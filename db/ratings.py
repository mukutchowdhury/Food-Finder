"""
ratings.py: the interface to our restaurant rating data.
"""
import random

BIG_NUM = 100_000_000_000_000_000_000
ID_LEN = 12

MOCK_ID = '0' * ID_LEN

TEST_RESTAURANT_NAME = 'Food Store'
USER_ID = 'user_id'
REVIEW = 'review'
STAR = 'star'


ratings = {
    'Terrific Tacos': {
        USER_ID: 1,
        REVIEW: 'The tacos were bad',
        STAR: 2,
    },
    TEST_RESTAURANT_NAME: {
        USER_ID: 2,
        REVIEW: 'I liked the food',
        STAR: 5,
    },
}


def _get_test_name():
    name = 'test'
    new_part = random.randint(0, BIG_NUM)
    return name + str(new_part)


def get_test_rating():
    test_review = {}
    test_review[TEST_RESTAURANT_NAME] = _get_test_name()
    test_review[USER_ID] = 1000
    test_review[REVIEW] = 'cool'
    test_review[STAR] = 2
    return test_review


def get_ratings():
    return ratings


def _gen_id() -> str:
    _id = random.randint(0, BIG_NUM)
    _id = str(_id)
    _id = _id.rjust(ID_LEN, '0')
    return _id


def add_restaurant_rating(store_name: str,
                          user_id: int,
                          review: str,
                          star: int):
    newstar = int(star)
    if store_name is None or store_name == '' or store_name in ratings:
        raise ValueError('Fill out the restaurant name')
    if review is None or review == '':
        raise ValueError('Please provide a review')
    if newstar < 0:
        raise ValueError('Plese enter a positive number of stars')
    ratings[store_name] = {USER_ID: user_id,
                           REVIEW: review,
                           STAR: newstar}
    return _gen_id
