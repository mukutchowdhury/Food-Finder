"""
restaurants.py: the interface to our restaurant data.
"""

ADDRESS = 'restaurantAddress'
TEST_RESTAURANT_NAME = 'Food Store'

resturants = {
    'Terrific Tacos': {
        ADDRESS: '92 Water Ave',
    },
    TEST_RESTAURANT_NAME: {
        ADDRESS: '242 Chicken Street',
    },
}

def get_restaurants() -> dict:
    return resturants


def add_restaurant(store_name: str,  store_address: str):
    if store_name in resturants:
        raise ValueError(f'Error duplicate restaurant name: {store_name=}')
    if len(store_name) == 0:
        raise ValueError('Fill out the restaurant name')
    resturants[store_name] = {ADDRESS: store_address}