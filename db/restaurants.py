"""
restaurants.py: the interface to our restaurant data.
"""

ADDRESS = 'address'
ZIPCODE = 'zipcode'
NAME = 'name'
OWNER_ID = 'owner_id'
RESTAURANT_ID = 'restaurant_id'

resturants = {
    "User_1": {
        NAME: "Taco Spot",
        ADDRESS: "92 Water Ave",
        ZIPCODE: "10004",
        OWNER_ID: 1,
        RESTAURANT_ID: 9
    },
    "User_2": {
        NAME: "Italian Spot",
        ADDRESS: "242 Chicken Street",
        ZIPCODE: "10004",
        OWNER_ID: 23,
        RESTAURANT_ID: 12
    },
}


def get_nearby_restaurants(zip_code: str):
    nearby_rest = {}
    for rest_key in resturants:
        if (resturants[rest_key][ZIPCODE] == zip_code):
            nearby_rest = resturants[rest_key]
    return nearby_rest


def add_restaurant(store_name: str,  store_address: str, store_zipcode: str, store_owner_id: int):
    pass
