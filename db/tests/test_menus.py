import pytest

import db.menus as menu
import db.restaurants as rest


TEST_RESTAURANT = {
    rest.NAME: 'TEST',
    rest.ADDRESS: 'TEST',
    rest.ZIPCODE: 'TEST',
    rest.OWNER_ID: 1,
    rest.IMAGE: '',
    rest.PHONE: 'TEST',
    rest.CUISINE: [],
    rest.KEYWORDS: [],
    rest.CATEGORY: []
}

TEST_MENUITEM = {
    menu.NAME: 'Test',
    menu.DESCRIPTION: 'Test Description',
    menu.PRICE: 9.99,
    menu.CATEGORY: 'Test'
}

RESTAURANT_ID = 'restaurant_id'
MENUITEM_ID = 'menuitem_id'
TEST_UPDATE_PRICE = 11.99

@pytest.fixture(scope='function')
def temp_menu():
    restaurantid = rest.add_restaurant(TEST_RESTAURANT)[RESTAURANT_ID]
    menuitemid = menu.add_item_to_menu(restaurantid, TEST_MENUITEM)
    yield restaurantid, menuitemid[MENUITEM_ID]
    if menu.restaurant_exists(restaurantid):
        rest.del_restaurant(restaurantid)
    if menu.menu_exists(menuitemid):
        menu.del_item_from_menu(menuitemid)


def test_gen_menuitemid():
    _id = menu._gen_menuitemId()
    assert isinstance(_id, str)
    assert len(_id) == menu.ID_LEN


def test_get_restuarant_menu(temp_menu):
    restaurantid, menuitemid = temp_menu
    menuitems = menu.get_restuarant_menu(restaurantid)
    assert isinstance(menuitems, list)
    for menuitem in menuitems:
        assert isinstance(menuitem, dict)
    assert menu.menu_exists(menuitemid)
    assert menu.restaurant_exists(restaurantid)


def test_get_restuarant_menu_NotFound():
    with pytest.raises(ValueError):
        menu.get_restuarant_menu(0)


def test_add_item_to_menu(temp_menu):
    restaurantid, _menuitemid = temp_menu
    ret = menu.add_item_to_menu(restaurantid, TEST_MENUITEM)
    assert isinstance(ret, dict)
    assert menu.menu_exists(ret[menu.MENUITEM_ID])


def test_add_item_to_menu_NotFound(temp_menu):
    with pytest.raises(ValueError):
        menu.add_item_to_menu(1, TEST_MENUITEM)


def test_add_item_to_menu_Blank(temp_menu):
    restaurantid, _menuitemid = temp_menu
    with pytest.raises(ValueError):
        menu.add_item_to_menu(restaurantid, {
            menu.NAME: '',
            menu.DESCRIPTION: '',
            menu.PRICE: 0,
            menu.CATEGORY: ''
        })


def test_update_price(temp_menu): 
    _restaurantid, menuitemid = temp_menu
    menu.update_price(menuitemid, TEST_UPDATE_PRICE)
    assert menu.menu_exists(menuitemid)


def test_update_price_NotFound():
    with pytest.raises(ValueError):
        menu.update_price(0, TEST_UPDATE_PRICE)


def test_del_item_from_menu(temp_menu):
    _restaurantid, menuitemid = temp_menu
    menu.del_item_from_menu(menuitemid)
    assert not menu.menu_exists(menuitemid)


def test_del_item_from_menu_NotFound():
    with pytest.raises(ValueError):
        menu.del_item_from_menu(0)
