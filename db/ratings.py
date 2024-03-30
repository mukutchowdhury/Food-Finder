import db.db_connect as dbc

import random

ID_LEN = 24
BIG_NUM = 100_000_000_000_000_000_000

MOCK_ID = '0' * ID_LEN

REVIEW_ID = 'review_id'
RESTAURANT_ID = 'restaurant_id'
USER_ID = 'user_id'
TEXT = 'text'
STAR = 'star'
RATING_COLLECT = 'ratings'
RATING_DB = 'ratingsdb'
REST_COLLECT = 'restaurants'


def _gen_reviewId() -> str:
    _id = random.randint(0, BIG_NUM)
    _id = str(_id)
    _id = _id.rjust(ID_LEN, '0')
    return _id


def review_exists(review_id: str) -> bool:
    dbc.connect_db()
    return dbc.fetch_one(RATING_COLLECT, {REVIEW_ID: review_id})


def restaurant_exists(restaurant_id: int) -> bool:
    dbc.connect_db()
    return dbc.fetch_one(REST_COLLECT, {RESTAURANT_ID: restaurant_id})


def get_restaurant_ratings(restaurant_id: int):
    if restaurant_exists(restaurant_id):
        return dbc.fetch_all_by_key(RATING_COLLECT,
                                    {RESTAURANT_ID: restaurant_id})
    raise ValueError(f'Get failure: {restaurant_id} not found.')


def add_restaurant_rating(restaurant_id: int, user_id: int,
                          text: str, star: int):
    if not restaurant_exists(restaurant_id):
        raise ValueError(f'Post failure: {restaurant_id} not found.')
    if not (restaurant_id and user_id and text and star):
        raise ValueError("All attributes must be filled out")
    review_Id = _gen_reviewId()
    star_adjusted = min(max(star, 1), 5)
    rating = {
        REVIEW_ID: review_Id,
        RESTAURANT_ID: restaurant_id,
        USER_ID: user_id,
        TEXT: text,
        STAR: star_adjusted
    }
    dbc.connect_db()
    _id = dbc.insert_one(RATING_COLLECT, rating)
    return {
        "status": _id is not None,
        "review_id": review_Id
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
