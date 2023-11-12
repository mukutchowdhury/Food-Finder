import pytest

import db.menus as menu


def test_add_item_to_menu_new():
    restaurant_id = 312 # Restaurant ID doesn't exists
    item_info = {
        "item_name": "Test",
        "item_description": "Test Description",
        "item_price": 1.99,
        "item_category": "Test"
    }

    menu.add_item_to_menu(restaurant_id, item_info)

    rest_menu = menu.get_restuarant_menu(restaurant_id)
    assert isinstance(rest_menu, dict)
    assert item_info["item_name"] in rest_menu


    # all_menu_items = menu.get_all_menu_items()
    # assert restaurant_id in all_menu_items
    # assert item_info["item_name"] in menu.get_all_menu_items()[restaurant_id]


def test_add_item_to_menu_existing():
    restaurant_id = 2 # Restaurant ID exists
    item_info = {
        "item_name": "Test",
        "item_description": "Test Description",
        "item_price": 1.99,
        "item_category": "Test"
    }

    menu.add_item_to_menu(restaurant_id, item_info)

    rest_menu = menu.get_restuarant_menu(restaurant_id)
    assert isinstance(rest_menu, dict)
    assert item_info["item_name"] in rest_menu


def test_add_existing_item():
    restaurant_id = 2
    item_info = {
        "item_name": "Tacos",
        "item_description": "Test Description",
        "item_price": 1.99,
        "item_category": "Test"
    }

    with pytest.raises(ValueError):  
        menu.add_item_to_menu(restaurant_id, item_info)


def test_add_empty_item():
    restaurant_id = 42
    item_info = {
        "item_name": "",
        "item_description": "",
        "item_price": 0.00,
        "item_category": ""
    }

    with pytest.raises(ValueError):  
        menu.add_item_to_menu(restaurant_id, item_info)


def test_remove_item_from_menu():
    restaurant_id = 2
    item_name = "Pasta"

    menu.remove_item_from_menu(restaurant_id, item_name)
    assert item_name not in menu.get_restuarant_menu(restaurant_id)


def test_remove_item_no_restaurant():
    restaurant_id = 41
    item_name = "Test"

    with pytest.raises(ValueError):
        menu.remove_item_from_menu(restaurant_id, item_name)


def test_remove_item_doesnt_exists():
    restaurant_id = 2
    item_name = "Test_23"

    with pytest.raises(ValueError):
        menu.remove_item_from_menu(restaurant_id, item_name)
    


def test_get_restuarant_menu():
    restaurant_id = 2
    result = menu.get_restuarant_menu(restaurant_id)
    assert isinstance(result, dict)
    for item_key in result:
        assert isinstance(item_key, str)
        item = result[item_key]
        assert isinstance(item, dict)
        assert menu.ITEM_CATEGORY in item
        assert menu.ITEM_PRICE in item
        assert menu.ITEM_DESCRIPTION in item

        assert isinstance(item[menu.ITEM_CATEGORY], str)
        assert isinstance(item[menu.ITEM_DESCRIPTION], str)
        assert isinstance(item[menu.ITEM_PRICE], float)


def test_get_restuarant_menu():
    restaurant_id = 2
    result = menu.get_restuarant_menu(restaurant_id)
    assert isinstance(result, dict)
    for item_key in result:
        assert isinstance(item_key, str)
        item = result[item_key]
        assert isinstance(item, dict)
        assert menu.ITEM_CATEGORY in item
        assert menu.ITEM_PRICE in item
        assert menu.ITEM_DESCRIPTION in item

        assert isinstance(item[menu.ITEM_CATEGORY], str)
        assert isinstance(item[menu.ITEM_DESCRIPTION], str)
        assert isinstance(item[menu.ITEM_PRICE], float)


def test_get_restuarant_menu_bad():
    restaurant_id = 64
    with pytest.raises(ValueError):
        menu.get_restuarant_menu(restaurant_id)


def test_get_test_menu():
    test_menu = menu.get_test_menu()
    assert isinstance(test_menu, dict)
    

def test_get_test_restaurant_id():
    id = menu._get_test_restaurant_id()
    assert isinstance(id, int)