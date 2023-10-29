"""
addrestaurant.py: the menu of our restaurant
"""

MenuItem = {
    "Restaurant1": {
        "Menu": [
            {
                "item_name": "Burger",
                "item_description": "Delicious burger with cheese and Onions",
                "item_price": 9.99,
                "item_category": "Burgers"
            },
            {
                "item_name": "Pizza",
                "item_description": "Margherita pizza with fresh ingredients",
                "item_price": 13.99,
                "item_category": "Pizza"
            },
            {
                "item_name": "Salad",
                "item_description": "Salad with dressing",
                "item_price": 4.99,
                "item_category": "Salads"
            }
        ]
    },
    "Restaurant2": {
        "Menu": [
            {
                "item_name": "Tacos",
                "item_description": "Delicious meat with toppings",
                "item_price": 2.99,
                "item_category": "Tacos"
            },
            {
                "item_name": "Pasta",
                "item_description": "Spagetti with tomato sauce",
                "item_price": 8.99,
                "item_category": "Pizza"
            },
            {
                "item_name": "Gyro",
                "item_description": "Chicken over rice",
                "item_price": 12.00,
                "item_category": "Gyro"
            }
        ]
    },
}


def add_menu(restaurant_name, item_name, item_description,
            item_price, item_category):
    """
    Adds items information to the MenuItem
    """

    another_new_item = {
        "item_name": item_name,
        "item_description": item_description,
        "item_price": item_price,
        "item_category": item_category
    }

    MenuItem[restaurant_name]["Menu"].append(another_new_item)


def remove_item(restaurant_name, item_name):
    """
    Removes items information from the MenuItem
    """

    menu = MenuItem[restaurant_name]["Menu"]

    for i in menu:
        if i["item_name"] == item_name:
            menu.remove(i)
            return True
    return False


def get_menu():
    """
    No arguments, return menuitem
    """
    return MenuItem
