"""
ratings.py: the interface to our restaurant rating data.
"""
import random

import db.db_connect as dbc

BIG_NUM = 1_000_000_000
ID_LEN = 12

MOCK_ID = '0' * ID_LEN

REVIEW_ID = 'review_id'
RESTAURANT_ID = 'restaurant_id'
USER_ID = 'user_id'
TEXT = 'text'
STAR = 'star'

RATING_COLLECT = 'ratings'
RATING_DB = 'ratingsdb'

REST_COLLECT = 'restaurants'

ratings = {}


# def _get_test_name():
#     name = 'test'
#     new_part = random.randint(0, BIG_NUM)
#     return name + str(new_part)


# def get_test_rating():
#     test_review = {}
#     test_review[RESTAURANT_NAME] = _get_test_name()
#     test_review[USER_ID] = 1000
#     test_review[REVIEW] = 'cool'
#     test_review[STAR] = 2
#     return test_review


# def _gen_id() -> str:
#     _id = random.randint(0, BIG_NUM)
#     _id = str(_id)
#     _id = _id.rjust(ID_LEN, '0')
#     return _id

# GOOD

def review_exists(review_id: int) -> bool:
    dbc.connect_db()
    return dbc.fetch_one(RATING_COLLECT, {REVIEW_ID: review_id})


def rest_exists(restaurant_id: int) -> bool:
    dbc.connect_db()
    return dbc.fetch_one(REST_COLLECT, {RESTAURANT_ID: restaurant_id})


def exists(restaurant_id: int) -> bool:
    dbc.connect_db()
    return dbc.fetch_one(RATING_COLLECT, {RESTAURANT_ID: restaurant_id})


def get_all_ratings(restaurant_id: int):
    if exists(restaurant_id):
        return dbc.fetch_all_by_key(RATING_COLLECT, {RESTAURANT_ID: restaurant_id})
    raise ValueError(f'Get failure: {restaurant_id} not found.')


def add_restaurant_rating(restaurant_id: int, user_id: int,
                          text: str, star: int):

    if not rest_exists(restaurant_id):
        raise ValueError(f'Post failure: {restaurant_id} not found.')

    if not (restaurant_id and user_id and text and star):
        raise ValueError("All attributes must be filled out")

    review_id = random.randint(0, BIG_NUM)
    while review_exists(review_id):
        review_id = random.randint(0, BIG_NUM)

    if star <= 1:
        star = 1
    elif star >= 5:
        star = 5

    rating = {
        REVIEW_ID: review_id,
        RESTAURANT_ID: restaurant_id,
        USER_ID: user_id,
        TEXT: text,
        STAR: star
    }

    dbc.connect_db()
    _id = dbc.insert_one(RATING_COLLECT, rating)

    return {
        'status': _id is not None,
        'review_id': review_id
    }


def update_review_text(review_id: int, text: str):
    if review_exists(review_id):
        return dbc.up_one(
            RATING_COLLECT,
            {REVIEW_ID: review_id},
            {"$set": {TEXT: text}}
        )
    raise ValueError(f'Update failure: Review: {review_id} not in database.')


def del_rating(review_id: int):
    if review_exists(review_id):
        return dbc.del_one(
            RATING_COLLECT,
            {REVIEW_ID: review_id}
        )
    raise ValueError(f'Delete failure: Review: {review_id} not in database.')
