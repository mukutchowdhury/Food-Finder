import pytest

import db.addrestaurantmenu as menu


def test_get_menu():
    gen_menu = menu.get_menu()
    assert isinstance(gen_menu, dict)
    for rest_key in gen_menu:
        assert isinstance(rest_key, str)
        rest_menu = gen_menu[rest_key]
        assert isinstance(rest_menu, dict)

        for item in range(len(rest_menu['Menu'])):
            assert menu.ITEM_NAME in rest_menu['Menu'][item]
            assert menu.ITEM_DESCRIPTION in rest_menu['Menu'][item]
            assert menu.ITEM_PRICE in rest_menu['Menu'][item]
            assert menu.ITEM_CATEGORY in rest_menu['Menu'][item]

            assert isinstance(rest_menu['Menu'][item][menu.ITEM_NAME], str)
            assert isinstance(rest_menu['Menu'][item][menu.ITEM_DESCRIPTION], str)
            assert isinstance(rest_menu['Menu'][item][menu.ITEM_PRICE], float)
            assert isinstance(rest_menu['Menu'][item][menu.ITEM_CATEGORY], str)


def test_add_restaurant():
    restaurant_name = "Restaurant1"
    item_name = 'sushi'
    item_description = 'fish with rice wrapped in seaweed'
    item_price = 8.00
    item_category = 'sushi'
    menu.add_menu(restaurant_name, item_name, item_description, item_price, item_category)
    new_menu =  menu.get_menu()[restaurant_name]['Menu']
    assert item_name in new_menu[len(new_menu) - 1][menu.ITEM_NAME]


def test_duplicate_item_name():
    restaurant_name = "Restaurant1"
    item_name = 'Burger'
    item_description = 'rice, fish, seaweed'
    item_price = 5.99
    item_category = 'Burger'
    with pytest.raises(ValueError):
        menu.add_menu(restaurant_name, item_name, item_description, item_price, item_category)


def test_empty_menu_input():
    restaurant_name = ""
    item_name = 'sushi'
    item_description = 'rice, fish, seaweed'
    item_price = 5.99
    item_category = ''
    with pytest.raises(ValueError):
        menu.add_menu(restaurant_name, item_name, item_description, item_price, item_category)

