"""
ratings.py: the interface to our restaurant rating data.
"""

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


def get_ratings():
    return ratings


def add_restaurant_rating(store_name: str,
                          user_id: int,
                          review: str,
                          star: int):
    newstar = int(star)
    if store_name is None or store_name == '':
        raise ValueError('Fill out the restaurant name')
    if review is None or review == '':
        raise ValueError('Please provide a review')
    if newstar < 0:
        raise ValueError('Plese enter a positive number of stars')
    ratings[store_name] = {USER_ID: user_id,
                           REVIEW: review,
                           STAR: newstar}
