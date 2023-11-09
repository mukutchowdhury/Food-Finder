from http.client import (
    BAD_REQUEST,
    FORBIDDEN,
    NOT_ACCEPTABLE,
    NOT_FOUND,
    OK,
    SERVICE_UNAVAILABLE,
)

from unittest.mock import patch

import server.endpoints as ep
import db.restaurants as rest

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

def test_addmenuitem():
    # return successfully added message
    user_json = {"restaurant_name": "Restaurant1", "item_name": "Spagetti", "item_description": "spicy", "item_price": 5.68, "item_category": "Spagetti"}
    resp = TEST_CLIENT.post(ep.ADD_RESTAURANT_MENUITEM, json=user_json)
    assert resp.status_code == 201
    resp_json = resp.get_json()
    assert "MENU_STATUS" in resp_json
    print(f'RestaurantMenu: {resp_json["MENU_STATUS"]}')
    assert "PASS" in resp_json["MENU_STATUS"]



### Restaurant Registration Tests ###
def test_restaurant_registration():
    user_json = {
        "rest_name": "Imperial Fish", 
        "rest_address": "439 Somewhere St", 
        "rest_zipcode": "10002"
    }
    resp = TEST_CLIENT.post(ep.RESTAURANT_REGISTRATION, json=user_json)
    assert resp.status_code == 200
    resp_json = resp.get_json()
    assert "SYSTEM_STATUS" in resp_json
    print(f'Restaurant Registrated: {resp_json["SYSTEM_STATUS"]}')
    assert "PASSED" in resp_json["SYSTEM_STATUS"]



@patch('db.restaurants.add_restaurant', side_effect=ValueError, autospec=True)
def test_existing_restaurant_registration(mock_add):
    resp = TEST_CLIENT.post(ep.RESTAURANT_REGISTRATION, json=rest.get_test_restaurant())
    assert resp.status_code == 406


def test_empty_restaurant_registration():
    user_json = {
        "rest_name": "", 
        "rest_address": "", 
        "rest_zipcode": ""
    }
    resp = TEST_CLIENT.post(ep.RESTAURANT_REGISTRATION, json=user_json)
    assert resp.status_code == 406
    resp_json = resp.get_json()
    assert "SYSTEM_STATUS" in resp_json
    print(f'Restaurant Registrated: {resp_json["SYSTEM_STATUS"]}')
    assert "FAILED" in resp_json["SYSTEM_STATUS"]

