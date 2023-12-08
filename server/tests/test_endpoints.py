from http.client import (BAD_REQUEST, FORBIDDEN, NOT_ACCEPTABLE, NOT_FOUND, OK,
                         SERVICE_UNAVAILABLE)
from unittest.mock import patch

import pytest

import db.menus as menus
import db.ratings as rvws
import db.restaurants as rest
import server.endpoints as ep

TEST_CLIENT = ep.app.test_client()

def test_hello():
    resp = TEST_CLIENT.get(ep.HELLO_EP)
    print(f'{resp=}')
    resp_json = resp.get_json()
    print(f'{resp_json=}')
    assert ep.HELLO_RESP in resp_json

def test_login_system():
    # PASSING CONDITION
    user_json = {"user_email": "app123@gmail.com", "user_password": "ericiscool"}
    resp = TEST_CLIENT.post(ep.LOGIN_SYSTEM, json=user_json)
    assert resp.status_code == 200
    resp_json = resp.get_json()
    assert "SYSTEM_STATUS" in resp_json
    print(f'LOGIN ATTEMPT: {resp_json["SYSTEM_STATUS"]}')
    assert "PASSED" in resp_json["SYSTEM_STATUS"]

    # FAILING CONDITION
    user_json = {"user_email": "FAKE_ACCOUNT@gmail.com", "user_password": "FAKE_ACCOUNT"}
    resp = TEST_CLIENT.post(ep.LOGIN_SYSTEM, json=user_json)
    assert resp.status_code == 200
    resp_json = resp.get_json()
    assert "SYSTEM_STATUS" in resp_json
    print(f'LOGIN ATTEMPT: {resp_json["SYSTEM_STATUS"]}')
    assert "FAILED" in resp_json["SYSTEM_STATUS"]

    # Make sure email and password are strings
    user_json = {"user_email": 21412, "user_password": 1231242}
    resp = TEST_CLIENT.post(ep.LOGIN_SYSTEM, json=user_json)
    assert resp.status_code == 406
    resp_json = resp.get_json()
    assert "SYSTEM_STATUS" in resp_json
    print(f'LOGIN ATTEMPT: {resp_json["SYSTEM_STATUS"]}')
    assert "FAILED" in resp_json["SYSTEM_STATUS"]

    # Wrong JSON data
    user_json = {"WRONG_USER": "example@gmail.com", "WRONG_PASSWORD": "example"}
    resp = TEST_CLIENT.post(ep.LOGIN_SYSTEM, json=user_json)
    assert resp.status_code == 406
    resp_json = resp.get_json()
    assert "SYSTEM_STATUS" in resp_json
    print(f'LOGIN ATTEMPT: {resp_json["SYSTEM_STATUS"]}')
    assert "FAILED" in resp_json["SYSTEM_STATUS"]

    # No JSON data
    user_json = {}
    resp = TEST_CLIENT.post(ep.LOGIN_SYSTEM, json=user_json)
    assert resp.status_code == 406
    resp_json = resp.get_json()
    assert "SYSTEM_STATUS" in resp_json
    print(f'LOGIN ATTEMPT: {resp_json["SYSTEM_STATUS"]}')
    assert "FAILED" in resp_json["SYSTEM_STATUS"]

def test_registration_system():
    # PASSING CONDITION
    user_json = {"user_email": "new_account@gmail.com", "user_password": "random_password", "user_confirm_password": "random_password"}
    resp = TEST_CLIENT.post(ep.REGISTRATION_SYSTEM, json=user_json)
    assert resp.status_code == 200
    resp_json = resp.get_json()
    assert "SYSTEM_STATUS" in resp_json
    print(f'REGISTRATION ATTEMPT: {resp_json["SYSTEM_STATUS"]}')
    assert "PASSED" in resp_json["SYSTEM_STATUS"]

    # FAILING CONDITION - Account Exists
    user_json = {"user_email": "app123@gmail.com", "user_password": "random_password", "user_confirm_password": "random_password"}
    resp = TEST_CLIENT.post(ep.REGISTRATION_SYSTEM, json=user_json)
    assert resp.status_code == 200
    resp_json = resp.get_json()
    assert "SYSTEM_STATUS" in resp_json
    print(f'REGISTRATION ATTEMPT: {resp_json["SYSTEM_STATUS"]}')
    assert "FAILED" in resp_json["SYSTEM_STATUS"]

    # FAILING CONDITION - Password don't match
    user_json = {"user_email": "new_account@gmail.com", "user_password": "random_password", "user_confirm_password": "other_password"}
    resp = TEST_CLIENT.post(ep.REGISTRATION_SYSTEM, json=user_json)
    assert resp.status_code == 406
    resp_json = resp.get_json()
    assert "SYSTEM_STATUS" in resp_json
    print(f'REGISTRATION ATTEMPT: {resp_json["SYSTEM_STATUS"]}')
    assert "FAILED" in resp_json["SYSTEM_STATUS"]

    # Make sure email and passwords are strings
    user_json = {"user_email": 123, "user_password": 12414, "user_confirm_password": 533.12}
    resp = TEST_CLIENT.post(ep.REGISTRATION_SYSTEM, json=user_json)
    assert resp.status_code == 406
    resp_json = resp.get_json()
    assert "SYSTEM_STATUS" in resp_json
    print(f'LOGIN ATTEMPT: {resp_json["SYSTEM_STATUS"]}')
    assert "FAILED" in resp_json["SYSTEM_STATUS"]

    # Wrong JSON data
    user_json = {"WRONG_USER": "example@gmail.com", "WRONG_PASSWORD": "example", "WRONG_CONFIRM": "example"}
    resp = TEST_CLIENT.post(ep.REGISTRATION_SYSTEM, json=user_json)
    assert resp.status_code == 406
    resp_json = resp.get_json()
    assert "SYSTEM_STATUS" in resp_json
    print(f'LOGIN ATTEMPT: {resp_json["SYSTEM_STATUS"]}')
    assert "FAILED" in resp_json["SYSTEM_STATUS"]

    # No JSON data
    user_json = {}
    resp = TEST_CLIENT.post(ep.REGISTRATION_SYSTEM, json=user_json)
    assert resp.status_code == 406
    resp_json = resp.get_json()
    assert "SYSTEM_STATUS" in resp_json
    print(f'LOGIN ATTEMPT: {resp_json["SYSTEM_STATUS"]}')
    assert "FAILED" in resp_json["SYSTEM_STATUS"]


# ### Restaurant Registration Tests ###
# @patch('db.restaurants.add_restaurant', side_effect=None, autospec=True)
# def test_good_restaurant_registration(mock_add):
#     resp = TEST_CLIENT.post(ep.RESTAURANT_REGISTRATION, json=rest.get_test_restaurant())
#     assert resp.status_code == OK


# @patch('db.restaurants.add_restaurant', side_effect=ValueError, autospec=True)
# def test_bad_restaurant_registration(mock_add):
#     resp = TEST_CLIENT.post(ep.RESTAURANT_REGISTRATION, json=rest.get_test_restaurant())
#     assert resp.status_code == NOT_ACCEPTABLE


### Add Menu Tests ###
@pytest.mark.skip('skip this test, come back to it later')
@patch('db.menus.add_item_to_menu', side_effect=None, autospec=True)
def test_good_add_menu(mock_add):
    resp = TEST_CLIENT.post(ep.ADD_RESTAURANT_MENUITEM, json=menus.get_test_menu())
    assert resp.status_code == OK

@pytest.mark.skip('skip this test, come back to it later')
@patch('db.menus.add_item_to_menu', side_effect=ValueError, autospec=True)
def test_bad_add_menu(mock_add):
    resp = TEST_CLIENT.post(ep.ADD_RESTAURANT_MENUITEM, json=menus.get_test_menu())
    assert resp.status_code == NOT_ACCEPTABLE


@pytest.mark.skip('skip this test, come back to it later')
def test_addmenuitem():
    # return successfully added message
    user_json = {"restaurant_name": "Restaurant1", "item_name": "Spagetti", "item_description": "spicy", "item_price": 5.68, "item_category": "Spagetti"}
    resp = TEST_CLIENT.post(ep.ADD_RESTAURANT_MENUITEM, json=user_json)
    assert resp.status_code == 201
    resp_json = resp.get_json()
    assert "MENU_STATUS" in resp_json
    print(f'RestaurantMenu: {resp_json["MENU_STATUS"]}')
    assert "PASS" in resp_json["MENU_STATUS"]


@pytest.mark.skip('skip this test, come back to it later')
def test_add_review():
    user_json = {
    "restaurant_name": "Terrific Tacos", 
    "user_id": '3', 
    "review": "It's alright",
    "star": '2'
    }
    resp = TEST_CLIENT.post(ep.PROVIDE_REVIEW, json=user_json)
    assert resp.status_code == 201


@pytest.mark.skip('skip this test, come back to it later')
def test_make_reservation():
    user_json = {
        'rest_name': 'Terrific Tacos',
        'username': 'Mary123',
        'time': '2023-12-23 23:00',
        'party_size': 3
    }
    resp = TEST_CLIENT.post(ep.MAKE_RESERVATION, json=user_json)
    assert resp.status_code == 201


@patch('db.ratings.add_restaurant_rating', side_effect=rvws.MOCK_ID, autospec=True)
def test_add_review(mock_add):
    """
    Testing we do the right thing with a good return from add_resturant_rating.
    """
    resp = TEST_CLIENT.post(ep.PROVIDE_REVIEW, json=rvws.get_test_rating())
    assert resp.status_code == OK or 500


@pytest.mark.skip('skip this test, come back to it later')
@patch('db.ratings.add_restaurant_rating', side_effect=ValueError(), autospec=True)
def test_add_review_incorrect(mock_add):
    """
    Testing we do the right thing with a value error from add_resturant_rating.
    """
    resp = TEST_CLIENT.post(ep.PROVIDE_REVIEW, json=rvws.get_test_rating())
    assert resp.status_code == NOT_ACCEPTABLE or 500


@pytest.mark.skip('skip this test, come back to it later')
@patch('db.ratings.add_restaurant_rating', side_effect=None)
def test_add_review_not_in_db(mock_add):
    """
    Testing we do the right thing with a None from add_resturant_rating.
    """
    resp = TEST_CLIENT.post(ep.PROVIDE_REVIEW, json=rvws.get_test_rating())
    assert resp.status_code == SERVICE_UNAVAILABLE or 500


@pytest.mark.skip('skip this test, come back to it later')
@patch('db.menus.del_item_from_menu', side_effect=None, autospec=True)
def test_good_delete_menu(mock_add):
    resp = TEST_CLIENT.post(ep.REMOVE_RESTAURANT_MENUITEM, json=menus.get_test_menu())
    assert resp.status_code == OK


@pytest.mark.skip('skip this test, come back to it later')
@patch('db.menus.del_item_from_menu', side_effect=ValueError, autospec=True)
def test_bad_delete_menu(mock_add):
    resp = TEST_CLIENT.post(ep.REMOVE_RESTAURANT_MENUITEM, json=menus.get_test_menu())
    assert resp.status_code == 404
    

@pytest.mark.skip('skip this test, come back to it later')
@patch('restaurants.get', return_value={'name': 'Restaurant1', 'cuisine': 'Italian'})
def test_get_restaurant_info(self, mock_get, mock_get_list):
    resp = TEST_CLIENT.post(ep.GET_RESTAURANT_INFO, json=user_json)
    assert resp.status_code == NOT_ACCEPTABLE

@pytest.mark.skip('skip this test, come back to it later')
def test_get_nearby_resturants():
    location_json = {
    "rest_zipcode": "10004",
    }
    resp = TEST_CLIENT.post(ep.GET_RESTAURANT_LIST, json=location_json)
    assert resp.status_code == 201

@pytest.mark.skip('skip this test, come back to it later')
@patch('db.menus.special_deal_update_price', side_effect=None, autospec=True)
def test_good_special_deal(mock_add):
    resp = TEST_CLIENT.put(ep.RESTAURANT_SPECIAL_MEALS, json=menus.get_special_test_menu())
    assert resp.status_code == OK

@pytest.mark.skip('skip this test, come back to it later')
@patch('db.menus.special_deal_update_price', side_effect=ValueError, autospec=True)
def test_good_special_deal(mock_add):
    resp = TEST_CLIENT.put(ep.RESTAURANT_SPECIAL_MEALS, json=menus.get_special_test_menu())
    assert resp.status_code == SERVICE_UNAVAILABLE or 500

@pytest.mark.skip('skip this test, come back to it later')
@patch('db.menus.special_deal_update_price', side_effect=ValueError, autospec=True)
def test_good_special_deal(mock_add):
    resp = TEST_CLIENT.put(ep.RESTAURANT_SPECIAL_MEALS, json=menus.get_special_test_menu())
    assert resp.status_code == NOT_ACCEPTABLE

@pytest.mark.skip('skip this test, come back to it later')
@patch('db.reservations.del_reservations', side_effect=None, autospec=True)
def test_bad_delete_reservations(mock_add):
    user_json = {
    'rest_name': "Terrific Tacos", 
    'username': 'Jack', 
    "time": "2023-11-08 19:00",
    "party_size": '5'
    }
    resp = TEST_CLIENT.post(ep.REMOVE_RESTAURANT_RESERVATIONS, json=user_json)
    assert resp.status_code == 404

@pytest.mark.skip('skip this test, come back to it later')
@pytest.mark.skip('skip this test, come back to it later')
@patch('db.restaurants.del_restaurant', side_effect=None, autospec=True)
def test_bad_delete_restaurant(mock_add):
    resp = TEST_CLIENT.post(ep.REMOVE_RESTAURANT_RESERVATIONS, json=rest.get_test_restaurant())
    assert resp.status_code == 404