"""
menus.py: the menu of our restaurant
"""

import random
import db.db_connect as dbc

ID_LEN = 24
BIG_NUM = 100_000_000_000_000_000_000

MOCK_ID = '0' * ID_LEN

MENUITEM_ID = 'menuitem_id'
RESTAURANT_ID = 'restaurant_id'
NAME = 'name'
DESCRIPTION = 'description'
PRICE = 'price'
CATEGORY = 'category'
IMAGE = 'image'

MENU_COLLECT = 'menus'
REST_COLLECT = 'restaurants'

STATUS = 'status'

NEW_PRICE = 'new_price'


def _gen_menuitemId() -> str:
    _id = random.randint(0, BIG_NUM)
    _id = str(_id)
    _id = _id.rjust(ID_LEN, '0')
    return _id


def get_test_menu():
    test_menu = {}
    test_menu[NAME] = 'TEST'
    test_menu[DESCRIPTION] = 'TEST'
    test_menu[PRICE] = 5.49
    test_menu[CATEGORY] = 'TEST'
    test_menu[IMAGE] = 'TEST'
    return test_menu


def get_test_add_return():
    test_return = {}
    test_return[STATUS] = MOCK_ID
    test_return[MENUITEM_ID] = _gen_menuitemId()
    return test_return


def get_test_bad_add_return():
    test_return = {}
    test_return[STATUS] = None
    test_return[MENUITEM_ID] = _gen_menuitemId()
    return test_return


def get_test_update_menuitem():
    return {NEW_PRICE: 9.99}


def menu_exists(menuitem_id: str) -> bool:
    dbc.connect_db()
    return dbc.fetch_one(MENU_COLLECT, {MENUITEM_ID: menuitem_id})


def restaurant_exists(restaurant_id: str) -> bool:
    dbc.connect_db()
    return dbc.fetch_one(REST_COLLECT, {RESTAURANT_ID: restaurant_id})


def get_restuarant_menu(restaurant_id: str) -> dict:
    if restaurant_exists(restaurant_id):
        return dbc.fetch_all_by_key(MENU_COLLECT,
                                    {RESTAURANT_ID: restaurant_id})
    raise ValueError(f'Get failure: {restaurant_id} not found.')


def add_item_to_menu(restaurant_id: str, item_info: dict):
    if not restaurant_exists(restaurant_id):
        raise ValueError(f'Post failure: {restaurant_id} not found.')
    if not (item_info[NAME] and item_info[PRICE]):
        raise ValueError("All attributes must be filled out")
    menuitem_id = _gen_menuitemId()
    while menu_exists(menuitem_id):
        menuitem_id = _gen_menuitemId()
    menu = {
        RESTAURANT_ID: restaurant_id,
        MENUITEM_ID: menuitem_id,
        NAME: item_info[NAME],
        DESCRIPTION: item_info[DESCRIPTION],
        PRICE: item_info[PRICE],
        CATEGORY: item_info[CATEGORY],
        IMAGE: item_info[IMAGE]
    }
    dbc.connect_db()
    _id = dbc.insert_one(MENU_COLLECT, menu)
    return {
        "status": _id is not None,
        "menuitem_id": menuitem_id
    }


def del_item_from_menu(menuitem_id: str):
    if menu_exists(menuitem_id):
        return dbc.del_one(
            MENU_COLLECT,
            {MENUITEM_ID: menuitem_id}
        )
    raise ValueError(f'Delete failure: MenuID: {menuitem_id} not in database.')


def update_price(menuitem_id: str, new_price: float):
    if menu_exists(menuitem_id):
        return dbc.up_one(
            MENU_COLLECT,
            {MENUITEM_ID: menuitem_id},
            {"$set": {PRICE: new_price}}
        )
    raise ValueError(f'Update failure: MenuID: {menuitem_id} not in database.')
