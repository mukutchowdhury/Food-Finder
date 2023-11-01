"""
restaurants.py: the interface to our restaurant data.
"""

ADDRESS = 'address'
ZIPCODE = 'zipcode'
NAME = 'name'
OWNER_ID = 'owner_id'
RESTAURANT_ID = 'restaurant_id'

# Make a list of all restaruant for all users; for now,
# one restaurant per user
restaurants = {
    "User_1": {
        NAME: "Taco Spot",
        ADDRESS: "92 Water Ave",
        ZIPCODE: "10004",
        OWNER_ID: 1,
        RESTAURANT_ID: 1
    },
    "User_2": {
        NAME: "Italian Spot",
        ADDRESS: "242 Chicken Street",
        ZIPCODE: "10002",
        OWNER_ID: 2,
        RESTAURANT_ID: 2
    },
    "User_3": {
        NAME: "Bonjour Spot",
        ADDRESS: "3 Wall Street",
        ZIPCODE: "10004",
        OWNER_ID: 3,
        RESTAURANT_ID: 3
    }
}


def get_restaurants():
    return restaurants


def get_nearby_restaurants(zip_code: str):
    nearby_rest = {}
    for rest_key in restaurants:
        if (restaurants[rest_key][ZIPCODE] == zip_code):
            nearby_rest[rest_key] = restaurants[rest_key]
    return nearby_rest


def add_restaurant(store_name: str,  store_address: str, store_zipcode: str):
    for rest_key in restaurants:
        rest = restaurants[rest_key]
        if (rest[ADDRESS] == store_address and
           rest[ZIPCODE] == store_zipcode):
            raise ValueError("Location already has a store")

        if not (store_name and store_address and store_zipcode):
            raise ValueError("All attributes must be filled out")

    new_entry = f'User_{len(restaurants)}'
    restaurants[new_entry] = {
        NAME: store_name,
        ADDRESS: store_address,
        ZIPCODE: store_zipcode,
        OWNER_ID: f'{len(restaurants)}',
        RESTAURANT_ID: f'{len(restaurants)}'
    }
