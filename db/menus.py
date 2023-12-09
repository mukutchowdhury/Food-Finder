"""
menus.py: the menu of our restaurant
"""

import random
import db.db_connect as dbc

BIG_NUM = 1_000_000_000

RESTAURANT_ID = 'restaurant_id'
ITEM_NAME = 'item_name'
ITEM_DESCRIPTION = 'item_description'
ITEM_PRICE = 'item_price'
ITEM_CATEGORY = 'item_category'

MENU_COLLECT = 'menus'
REST_COLLECT = 'restaurants'

MENU_DB = 'menudb'

MENUITEM_ID = 'menuitem_id'


menu_items = {}

# menu_items = {
#     1: {
#         "Burger": {
#             ITEM_DESCRIPTION: "Delicious burger with cheese and onions",
#             ITEM_PRICE: 9.99,
#             ITEM_CATEGORY: "Burgers"
#         },
#         "Pizza": {
#             ITEM_DESCRIPTION: "Margherita pizza with fresh ingredients",
#             ITEM_PRICE: 13.99,
#             ITEM_CATEGORY: "Pizza"
#         },
#         "Salad": {
#             ITEM_DESCRIPTION: "Salad with dressing",
#             ITEM_PRICE: 4.99,
#             ITEM_CATEGORY: "Salads"
#         },
#         "Expensive Dog Food": {
#             ITEM_DESCRIPTION: "It's in the name",
#             ITEM_PRICE: 99.99,
#             ITEM_CATEGORY: "NO"
#         }
#     },
#     2: {
#         "Tacos": {
#             ITEM_DESCRIPTION: "Delicious meat with toppings",
#             ITEM_PRICE: 2.99,
#             ITEM_CATEGORY: "Tacos"
#         },
#         "Pasta": {
#             ITEM_DESCRIPTION: "Spaghetti with tomato sauce",
#             ITEM_PRICE: 8.99,
#             ITEM_CATEGORY: "Pizza"
#         },
#         "Gyro": {
#             ITEM_DESCRIPTION: "Chicken over rice",
#             ITEM_PRICE: 12.00,
#             ITEM_CATEGORY: "Gyro"
#         }
#     }
# }


def _get_test_restaurant_id():
    return random.randint(0, BIG_NUM)


def get_test_menu():
    test_menu = {}
    test_menu[RESTAURANT_ID] = _get_test_restaurant_id()
    test_menu[ITEM_NAME] = 'TEST'
    test_menu[ITEM_DESCRIPTION] = 'TEST'
    test_menu[ITEM_PRICE] = 9.99
    test_menu[ITEM_CATEGORY] = 'TEST'
    return test_menu


def get_special_test_menu():
    test_menu = {}
    test_menu[RESTAURANT_ID] = _get_test_restaurant_id()
    test_menu[ITEM_NAME] = 'TEST'
    test_menu[ITEM_PRICE] = 2.99
    return test_menu


# GOOD
def get_restuarant_menu(restaurant_id: int) -> dict:
    if rest_exists(restaurant_id):
        return dbc.fetch_one(MENU_COLLECT, {RESTAURANT_ID: restaurant_id})
    raise ValueError(f'Get failure: {restaurant_id} not found.')


def menu_exists(menuitem_id: int) -> bool:
    dbc.connect_db()
    return dbc.fetch_one(MENU_COLLECT, {MENUITEM_ID: menuitem_id})


def rest_exists(restaurant_id: int) -> bool:
    dbc.connect_db()
    return dbc.fetch_one(REST_COLLECT, {RESTAURANT_ID: restaurant_id})


def add_item_to_menu(restaurant_id: int, item_info: dict):
    if not rest_exists(restaurant_id):
        raise ValueError(f'Post failure: {restaurant_id} not found.')

    if not (item_info['item_name'] and item_info['item_description']
            and item_info['item_price'] and item_info['item_category']):
        raise ValueError("All attributes must be filled out")

    menuitem_id = random.randint(0, BIG_NUM)
    while menu_exists(menuitem_id):
        menuitem_id = random.randint(0, BIG_NUM)

    menu = {
        RESTAURANT_ID: restaurant_id,
        MENUITEM_ID: menuitem_id,
        ITEM_NAME: item_info['item_name'],
        ITEM_DESCRIPTION: item_info['item_description'],
        ITEM_PRICE: item_info['item_price'],
        ITEM_CATEGORY: item_info['item_category']
    }

    dbc.connect_db()
    _id = dbc.insert_one(MENU_COLLECT, menu)
    return {
        "status": _id is not None,
        "restaurant_id": restaurant_id,
        "menuitem_id": menuitem_id
    }


def del_item_from_menu(restaurant_id: int, menuitem_id: int) -> None:
    if rest_exists(restaurant_id) and menu_exists(menuitem_id):
        return dbc.del_one(
            MENU_COLLECT,
            {RESTAURANT_ID: restaurant_id, MENUITEM_ID: menuitem_id}
        )
    raise ValueError(f'Delete failure: MenuID: {menuitem_id} ' +
                     f'and/or RestaurantID: {restaurant_id} not in database.')


def update_item_price(restaurant_id: int, menuitem_id: int, new_price: float):
    if rest_exists(restaurant_id) and menu_exists(menuitem_id):
        dbc.up_one(
            MENU_COLLECT,
            {RESTAURANT_ID: restaurant_id, MENUITEM_ID: menuitem_id},
            {"$set": {ITEM_PRICE: new_price}}
        )
    return ValueError(f'Update failure: MenuID: {menuitem_id}' +
                      f'and/or RestaurantID: {restaurant_id} not in database.')
