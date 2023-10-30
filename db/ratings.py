"""
ratings.py: the interface to our restaurant rating data.
"""

RATING = 'restaurantRating'
POSSIBLE_RATINGS = ['Terrible', 'Poor', 'Ok', 'Good', 'Excellent']
TEST_RESTAURANT_NAME = 'Food Store'

ratings = {
    'Terrific Tacos': {
        RATING: 'Terrible',
    },
    TEST_RESTAURANT_NAME: {
        RATING: 'Good',
    },
}


def get_ratings() -> dict:
    return ratings


def add_restaurant_rating(store_name: str,  store_rating: str):
    if store_name in ratings:
        raise ValueError(f'Error duplicate restaurant name: {store_name=}')
    if len(store_name) == 0:
        raise ValueError('Fill out the restaurant name')
    if store_rating not in POSSIBLE_RATINGS:
        raise ValueError('Error invalid restaurant rating')

    ratings[store_name] = {RATING: store_rating}
