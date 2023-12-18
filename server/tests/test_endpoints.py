from http.client import (
    BAD_REQUEST,
    FORBIDDEN,
    NOT_ACCEPTABLE,
    NOT_FOUND,
    OK,
    SERVICE_UNAVAILABLE,
)

from unittest.mock import patch
import pytest

import db.menus as menus
import db.ratings as rating
import db.restaurants as rest
import db.options as options

import server.endpoints as ep

TEST_CLIENT = ep.app.test_client()

def test_hello():
    resp = TEST_CLIENT.get(ep.HELLO_EP)
    print(f'{resp=}')
    resp_json = resp.get_json()
    print(f'{resp_json=}')
    assert ep.HELLO_RESP in resp_json


@patch('db.restaurants.add_restaurant', return_value=rest.MOCK_ID, autospec=True)
def test_add_restaurant(mock_add):
    resp = TEST_CLIENT.post(ep.ADD_RESTAURANT, json=rest.get_test_restaurant())
    assert resp.status_code == OK


@patch('db.restaurants.add_restaurant', side_effect=ValueError, autospec=True)
def test_bad_add_restaurant(mock_add):
    resp = TEST_CLIENT.post(ep.ADD_RESTAURANT, json=rest.get_test_restaurant())
    assert resp.status_code == NOT_ACCEPTABLE


@patch('db.restaurants.add_restaurant', return_value=None)
def test_restaurant_add_db_failure(mock_add):
    resp = TEST_CLIENT.post(ep.ADD_RESTAURANT, json=rest.get_test_restaurant())
    assert resp.status_code == SERVICE_UNAVAILABLE


@patch('db.restaurants.get_restuarant', return_value=None, autospec=True)
def test_get_restaurant(mock_get):
    resp = TEST_CLIENT.get(f'{ep.RESTAURANT_EP}/{rest.MOCK_ID}')
    assert resp.status_code == OK


@patch('db.restaurants.get_restuarant', side_effect=ValueError, autospec=True)
def test_bad_get_restaurant(mock_get):
    resp = TEST_CLIENT.get(f'{ep.RESTAURANT_EP}/{rest.MOCK_ID}')
    assert resp.status_code == NOT_FOUND


@patch('db.restaurants.del_restaurant', return_value=None, autospec=True)
def test_del_restaurant(mock_get):
    resp = TEST_CLIENT.delete(f'{ep.RESTAURANT_EP}/{rest.MOCK_ID}')
    assert resp.status_code == OK


@patch('db.restaurants.del_restaurant', side_effect=ValueError, autospec=True)
def test_bad_del_restaurant(mock_get):
    resp = TEST_CLIENT.delete(f'{ep.RESTAURANT_EP}/{rest.MOCK_ID}')
    assert resp.status_code == NOT_FOUND


def test_get_all_restaurant():
    resp = TEST_CLIENT.get(ep.RESTAURANT_ALL)
    assert resp.status_code == OK
    resp_json = resp.get_json()
    assert isinstance(resp_json, dict)


@patch('db.menus.get_restuarant_menu', return_value=None, autospec=True)
def test_get_menu(mock_get):
    resp = TEST_CLIENT.get(f'{ep.Menu_EP}/123')
    assert resp.status_code == OK


@patch('db.menus.get_restuarant_menu', side_effect=ValueError, autospec=True)
def test_bad_get_menu(mock_get):
    resp = TEST_CLIENT.get(f'{ep.Menu_EP}/123')
    assert resp.status_code == NOT_FOUND


# @patch('db.menus.add_item_to_menu', return_value=rest.MOCK_ID, autospec=True)
# def test_add_menu(mock_add):
#     resp = TEST_CLIENT.post(f'{ep.Menu_EP}/123', json=menus.get_test_menu())
#     assert resp.status_code == OK


@patch('db.menus.add_item_to_menu', side_effect=ValueError, autospec=True)
def test_bad_add_menu(mock_add):
    resp = TEST_CLIENT.post(f'{ep.Menu_EP}/123', json=menus.get_test_menu())
    assert resp.status_code == NOT_ACCEPTABLE


# @patch('db.menus.add_item_to_menu', return_value=None)
# def test_menu_add_db_failure(mock_add):
#     resp = TEST_CLIENT.post(f'{ep.Menu_EP}/123', json=menus.get_test_menu())
#     assert resp.status_code == SERVICE_UNAVAILABLE


# ### Add Menu Tests ###
# @pytest.mark.skip('skip this test, come back to it later')
# @patch('db.menus.add_item_to_menu', side_effect=None, autospec=True)
# def test_good_add_menu(mock_add):
#     resp = TEST_CLIENT.post(ep.ADD_RESTAURANT_MENUITEM, json=menus.get_test_menu())
#     assert resp.status_code == OK


# @pytest.mark.skip('skip this test, come back to it later')
# @patch('db.menus.add_item_to_menu', side_effect=ValueError, autospec=True)
# def test_bad_add_menu(mock_add):
#     resp = TEST_CLIENT.post(ep.ADD_RESTAURANT_MENUITEM, json=menus.get_test_menu())
#     assert resp.status_code == NOT_ACCEPTABLE


# @pytest.mark.skip('skip this test, come back to it later')
# def test_addmenuitem():
#     # return successfully added message
#     user_json = {"restaurant_name": "Restaurant1", "item_name": "Spagetti", "item_description": "spicy", "item_price": 5.68, "item_category": "Spagetti"}
#     resp = TEST_CLIENT.post(ep.ADD_RESTAURANT_MENUITEM, json=user_json)
#     assert resp.status_code == 201
#     resp_json = resp.get_json()
#     assert "MENU_STATUS" in resp_json
#     print(f'RestaurantMenu: {resp_json["MENU_STATUS"]}')
#     assert "PASS" in resp_json["MENU_STATUS"]


# @pytest.mark.skip('skip this test, come back to it later')
# def test_add_review():
#     user_json = {
#     "restaurant_name": "Terrific Tacos", 
#     "user_id": '3', 
#     "review": "It's alright",
#     "star": '2'
#     }
#     resp = TEST_CLIENT.post(ep.PROVIDE_REVIEW, json=user_json)
#     assert resp.status_code == 201


# @pytest.mark.skip('skip this test, come back to it later')
# def test_make_reservation():
#     user_json = {
#         'rest_name': 'Terrific Tacos',
#         'username': 'Mary123',
#         'time': '2023-12-23 23:00',
#         'party_size': 3
#     }
#     resp = TEST_CLIENT.post(ep.MAKE_RESERVATION, json=user_json)
#     assert resp.status_code == 201

# @pytest.mark.skip('skip this test, come back to it later')
# @patch('db.ratings.add_restaurant_rating', side_effect=rvws.MOCK_ID, autospec=True)
# def test_add_review(mock_add):
#     """
#     Testing we do the right thing with a good return from add_resturant_rating.
#     """
#     resp = TEST_CLIENT.post(ep.PROVIDE_REVIEW, json=rvws.get_test_rating())
#     assert resp.status_code == OK or 500


# @pytest.mark.skip('skip this test, come back to it later')
# @patch('db.ratings.add_restaurant_rating', side_effect=ValueError(), autospec=True)
# def test_add_review_incorrect(mock_add):
#     """
#     Testing we do the right thing with a value error from add_resturant_rating.
#     """
#     resp = TEST_CLIENT.post(ep.PROVIDE_REVIEW, json=rvws.get_test_rating())
#     assert resp.status_code == NOT_ACCEPTABLE or 500


# @pytest.mark.skip('skip this test, come back to it later')
# @patch('db.ratings.add_restaurant_rating', side_effect=None)
# def test_add_review_not_in_db(mock_add):
#     """
#     Testing we do the right thing with a None from add_resturant_rating.
#     """
#     resp = TEST_CLIENT.post(ep.PROVIDE_REVIEW, json=rvws.get_test_rating())
#     assert resp.status_code == SERVICE_UNAVAILABLE or 500


# @pytest.mark.skip('skip this test, come back to it later')
# @patch('db.menus.del_item_from_menu', side_effect=None, autospec=True)
# def test_good_delete_menu(mock_add):
#     resp = TEST_CLIENT.post(ep.REMOVE_RESTAURANT_MENUITEM, json=menus.get_test_menu())
#     assert resp.status_code == OK


# @pytest.mark.skip('skip this test, come back to it later')
# @patch('db.menus.del_item_from_menu', side_effect=ValueError, autospec=True)
# def test_bad_delete_menu(mock_add):
#     resp = TEST_CLIENT.post(ep.REMOVE_RESTAURANT_MENUITEM, json=menus.get_test_menu())
#     assert resp.status_code == 404
    

# @pytest.mark.skip('skip this test, come back to it later')
# @patch('restaurants.get', return_value={'name': 'Restaurant1', 'cuisine': 'Italian'})
# def test_get_restaurant_info(self, mock_get, mock_get_list):
#     resp = TEST_CLIENT.post(ep.GET_RESTAURANT_INFO, json=user_json)
#     assert resp.status_code == NOT_ACCEPTABLE

# @pytest.mark.skip('skip this test, come back to it later')
# def test_get_nearby_resturants():
#     location_json = {
#     "rest_zipcode": "10004",
#     }
#     resp = TEST_CLIENT.post(ep.GET_RESTAURANT_LIST, json=location_json)
#     assert resp.status_code == 201

# @pytest.mark.skip('skip this test, come back to it later')
# @patch('db.menus.special_deal_update_price', side_effect=None, autospec=True)
# def test_good_special_deal(mock_add):
#     resp = TEST_CLIENT.put(ep.RESTAURANT_SPECIAL_MEALS, json=menus.get_special_test_menu())
#     assert resp.status_code == OK

# @pytest.mark.skip('skip this test, come back to it later')
# @patch('db.menus.special_deal_update_price', side_effect=ValueError, autospec=True)
# def test_good_special_deal(mock_add):
#     resp = TEST_CLIENT.put(ep.RESTAURANT_SPECIAL_MEALS, json=menus.get_special_test_menu())
#     assert resp.status_code == SERVICE_UNAVAILABLE or 500

# @pytest.mark.skip('skip this test, come back to it later')
# @patch('db.menus.special_deal_update_price', side_effect=ValueError, autospec=True)
# def test_good_special_deal(mock_add):
#     resp = TEST_CLIENT.put(ep.RESTAURANT_SPECIAL_MEALS, json=menus.get_special_test_menu())
#     assert resp.status_code == NOT_ACCEPTABLE

# @pytest.mark.skip('skip this test, come back to it later')
# @patch('db.reservations.del_reservations', side_effect=None, autospec=True)
# def test_bad_delete_reservations(mock_add):
#     user_json = {
#     'rest_name': "Terrific Tacos", 
#     'username': 'Jack', 
#     "time": "2023-11-08 19:00",
#     "party_size": '5'
#     }
#     resp = TEST_CLIENT.post(ep.REMOVE_RESTAURANT_RESERVATIONS, json=user_json)
#     assert resp.status_code == 404

# @pytest.mark.skip('skip this test, come back to it later')
# @pytest.mark.skip('skip this test, come back to it later')
# @patch('db.restaurants.del_restaurant', side_effect=None, autospec=True)
# def test_bad_delete_restaurant(mock_add):
#     resp = TEST_CLIENT.post(ep.REMOVE_RESTAURANT_RESERVATIONS, json=rest.get_test_restaurant())
#     assert resp.status_code == 404


# @pytest.mark.skip('skip this test, come back to it later')
# @patch('db.restaurants.get_restaurants', side_effect=None, autospec=True)
# def test_get_restaurant_id(mock_add):
#     """
#     Testing with a good return from get_test_restaurant.

#     """
#     resp = TEST_CLIENT.post(ep.Restaurant_EP, json=rest.get_restaurants)
#     assert resp.status_code == OK


# @pytest.mark.skip('skip this test, come back to it later')
# @patch('db.restaurants.del_restaurant', side_effect=None, autospec=True)
# def test_delete_get_restaurant_id(mock_add):
#     """
#     Testing with a good delete return from get_test_restaurant.

#     """
#     resp = TEST_CLIENT.post(ep.Restaurant_EP, json=rest.del_restaurant)
#     assert resp.status_code == OK or 500

# @pytest.mark.skip('skip this test, come back to it later')
<<<<<<< HEAD
@patch('db.restaurants.add_restaurant', side_effect=None, autospec=True)
def test_register_add_restaurant(mock_add):
    """
    Testing with a restaurant entry

    """
    resp = TEST_CLIENT.post('/add-restaurant', json=rest.get_test_restaurant())
    assert resp.status_code == OK
=======
# @patch('db.restaurants.add_restaurant', side_effect=None, autospec=True)
# def test_register_add_restaurant(mock_add):
#     """
#     Testing with a restaurant entry

#     """
#     resp = TEST_CLIENT.post(ep.Add_Restaurant, json=rest.get_test_restaurant)
#     assert resp.status_code == OK
>>>>>>> 9dfd8203a1cf648563f98dd031bd8193c606e7f6







