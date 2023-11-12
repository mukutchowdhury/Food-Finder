"""
addrestaurant.py: the menu of our restaurant
"""

import random
BIG_NUM = 1_000_000_000

RESTAURANT_ID = 'restaurant_id'
ITEM_NAME = 'item_name'
ITEM_DESCRIPTION = 'item_description'
ITEM_PRICE = 'item_price'
ITEM_CATEGORY = 'item_category'

menu_items = {
    1: {
        "Burger": {
            ITEM_DESCRIPTION: "Delicious burger with cheese and onions",
            ITEM_PRICE: 9.99,
            ITEM_CATEGORY: "Burgers"
        },
        "Pizza": {
            ITEM_DESCRIPTION: "Margherita pizza with fresh ingredients",
            ITEM_PRICE: 13.99,
            ITEM_CATEGORY: "Pizza"
        },
        "Salad": {
            ITEM_DESCRIPTION: "Salad with dressing",
            ITEM_PRICE: 4.99,
            ITEM_CATEGORY: "Salads"
        },
        "Expensive Dog Food": {
            ITEM_DESCRIPTION: "It's in the name",
            ITEM_PRICE: 99.99,
            ITEM_CATEGORY: "NO"
        }
    },
    2: {
        "Tacos": {
            ITEM_DESCRIPTION: "Delicious meat with toppings",
            ITEM_PRICE: 2.99,
            ITEM_CATEGORY: "Tacos"
        },
        "Pasta": {
            ITEM_DESCRIPTION: "Spaghetti with tomato sauce",
            ITEM_PRICE: 8.99,
            ITEM_CATEGORY: "Pizza"
        },
        "Gyro": {
            ITEM_DESCRIPTION: "Chicken over rice",
            ITEM_PRICE: 12.00,
            ITEM_CATEGORY: "Gyro"
        }
    }
}


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


# unique item name per menu
def add_item_to_menu(restaurant_id: int, item_info: dict) -> None:
    """
    Adds items information to the MenuItem

    interface item_info {
        item_name: str,
        item_description: str,
        item_price: float,
        item_category: str
    }
    """
    # Assuming restaurant_id is valid and provided
    # (exists in the restaurants.py)
    item_name = item_info['item_name']
    if not item_name:
        raise ValueError("Missing Item Name")

    if restaurant_id not in menu_items:
        menu_items[restaurant_id] = {}
    else:
        if item_name in menu_items[restaurant_id]:
            raise ValueError("Item exists, unique constraint")

    menu_items[restaurant_id][item_name] = {
        ITEM_DESCRIPTION: item_info["item_description"],
        ITEM_PRICE: item_info["item_price"],
        ITEM_CATEGORY: item_info["item_category"]
    }


def remove_item_from_menu(restaurant_id: int, item_name: str) -> None:
    """
    Removes items information from the MenuItem
    """
    if restaurant_id not in menu_items:
        raise ValueError("restaurant doesn't exists")

    if item_name not in menu_items[restaurant_id]:
        raise ValueError("item doesn't exists")

    del menu_items[restaurant_id][item_name]


def get_restuarant_menu(restaurant_id: int) -> dict:
    """
    Get all menu items from restaurant
    """
    if (restaurant_id not in menu_items):
        raise ValueError("restaurant doesn't exists")
    return menu_items[restaurant_id]


# def get_all_menu_items() -> dict:
#     return menu_items
