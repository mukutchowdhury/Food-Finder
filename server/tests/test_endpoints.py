from http.client import (
    BAD_REQUEST,
    FORBIDDEN,
    NOT_ACCEPTABLE,
    NOT_FOUND,
    OK,
    CREATED,
    SERVICE_UNAVAILABLE,
)

from unittest.mock import patch
import pytest

import db.menus as menus
import db.ratings as rating
import db.restaurants as rest
import db.users as user
import db.categories as category

import server.endpoints as ep

TEST_CLIENT = ep.app.test_client()


# Users #
@patch('db.users.add_user', autospec=True)
def test_add_user(mock_add):
    resp = TEST_CLIENT.post(f'{ep.USER_EP}{ep.SIGN_UP}', json=user.get_test_user())
    assert resp.status_code == OK


@patch('db.users.add_user', side_effect=ValueError, autospec=True)
def test_bad_add_user(mock_add):
    resp = TEST_CLIENT.post(f'{ep.USER_EP}{ep.SIGN_UP}', json=user.get_test_user())
    assert resp.status_code == OK
    resp_json = resp.get_json()
    assert isinstance(resp_json, dict)


@patch('db.users.get_user', return_value=user.MOCK_ID, autospec=True)
def test_get_user(mock_add):
    resp = TEST_CLIENT.post(f'{ep.USER_EP}{ep.LOGIN}', json=user.get_test_login_user())
    assert resp.status_code == OK
    resp_json = resp.get_json()
    assert isinstance(resp_json, dict)


@patch('db.users.get_user', side_effect=ValueError, autospec=True)
def test_bad_get_user(mock_add):
    resp = TEST_CLIENT.post(f'{ep.USER_EP}{ep.LOGIN}', json=user.get_test_login_user())
    assert resp.status_code == OK
    resp_json = resp.get_json()
    assert isinstance(resp_json, dict)


@patch('db.users.get_userdata', return_value={}, autospec=True)
def test_get_userdata(mock_get):
    resp = TEST_CLIENT.get(f'{ep.USER_EP}/anyId')
    assert resp.status_code == OK
    resp_json = resp.get_json()
    assert isinstance(resp_json, dict)


@patch('db.users.get_userdata', side_effect=ValueError, autospec=True)
def test_bad_get_userdata(mock_get):
    resp = TEST_CLIENT.get(f'{ep.USER_EP}/anyId')
    assert resp.status_code == NOT_FOUND


def test_signup_form():
    resp = TEST_CLIENT.get(f'{ep.USER_EP}{ep.SIGNUP_FORM}')
    assert resp.status_code == OK
    resp_json = resp.get_json()
    assert isinstance(resp_json, list)
    assert isinstance(resp_json[0], dict)

# Restaurants #
@patch('db.restaurants.get_restaurant', return_value={}, autospec=True)
def test_get_restaurant(mock_get):
    resp = TEST_CLIENT.get(f'{ep.RESTAURANT_EP}/AnyId')
    assert resp.status_code == OK
    resp_json = resp.get_json()
    assert isinstance(resp_json, dict)


@patch('db.restaurants.get_restaurant', side_effect=ValueError, autospec=True)
def test_bad_get_restaurant(mock_get):
    resp = TEST_CLIENT.get(f'{ep.RESTAURANT_EP}/AnyId')
    assert resp.status_code == NOT_FOUND


@patch('db.restaurants.del_restaurant', autospec=True)
def test_del_restaurant(mock_delete):
    resp = TEST_CLIENT.delete(f'{ep.RESTAURANT_EP}/AnyId')
    assert resp.status_code == OK


@patch('db.restaurants.del_restaurant', side_effect=ValueError, autospec=True)
def test_bad_del_restaurant(mock_delete):
    resp = TEST_CLIENT.delete(f'{ep.RESTAURANT_EP}/AnyId')
    assert resp.status_code == NOT_FOUND


@patch('db.restaurants.add_restaurant', return_value=rest.get_test_add_return(), autospec=True)
def test_add_restaurant(mock_add):
    resp = TEST_CLIENT.post(f'{ep.RESTAURANT_EP}{ep.REGISTER}', json=rest.get_test_restaurant())
    assert resp.status_code == OK


@patch('db.restaurants.add_restaurant', side_effect=ValueError, autospec=True)
def test_bad_restaurant_add(mock_add):
    resp = TEST_CLIENT.post(f'{ep.RESTAURANT_EP}{ep.REGISTER}', json=rest.get_test_restaurant())
    assert resp.status_code == NOT_ACCEPTABLE


@patch('db.restaurants.add_restaurant', return_value=rest.get_test_bad_add_return(), autospec=True)
def test_restaurant_add_db_failure(mock_add):
    resp = TEST_CLIENT.post(f'{ep.RESTAURANT_EP}{ep.REGISTER}', json=rest.get_test_restaurant())
    assert resp.status_code == SERVICE_UNAVAILABLE


def test_get_all_restaurants():
    resp = TEST_CLIENT.get(f'{ep.RESTAURANT_EP}{ep.ALL}')
    assert resp.status_code == OK
    resp_json = resp.get_json()
    assert isinstance(resp_json, dict)


def test_get_restaurants_by_zipcode():
    resp = TEST_CLIENT.get(f'{ep.RESTAURANT_EP}{ep.BY_ZIPCODE}/anyZipcode')
    assert resp.status_code == OK
    resp_json = resp.get_json()
    assert isinstance(resp_json, dict)


@patch('db.restaurants.update_restaurant_time', autospec=True)
def test_update_restaurant_hour(mock_update):
    resp = TEST_CLIENT.put(f'{ep.RESTAURANT_EP}{ep.HOUR}/anyId', json=rest.get_test_update_hour())
    assert resp.status_code == OK


@patch('db.restaurants.update_restaurant_time', side_effect=ValueError, autospec=True)
def test_bad_update_restaurant_hour(mock_update):
    resp = TEST_CLIENT.put(f'{ep.RESTAURANT_EP}{ep.HOUR}/anyId', json=rest.get_test_update_hour())
    assert resp.status_code == NOT_FOUND


# Menus
@patch('db.menus.get_restuarant_menu', return_value=[], autospec=True)
def test_get_menu(mock_get):
    resp = TEST_CLIENT.get(f'{ep.MENU_EP}/AnyId')
    assert resp.status_code == OK
    resp_json = resp.get_json()
    assert isinstance(resp_json, list)


@patch('db.menus.get_restuarant_menu', side_effect=ValueError, autospec=True)
def test_bad_get_menu(mock_get):
    resp = TEST_CLIENT.get(f'{ep.MENU_EP}/AnyId')
    assert resp.status_code == NOT_FOUND


@patch('db.menus.add_item_to_menu', return_value=menus.get_test_add_return(), autospec=True)
def test_add_menu(mock_add):
    resp = TEST_CLIENT.post(f'{ep.MENU_EP}/AnyId', json=menus.get_test_menu())
    assert resp.status_code == OK


@patch('db.menus.add_item_to_menu', side_effect=ValueError, autospec=True)
def test_bad_add_menu(mock_add):
    resp = TEST_CLIENT.post(f'{ep.MENU_EP}/AnyId', json=menus.get_test_menu())
    assert resp.status_code == NOT_ACCEPTABLE


@patch('db.menus.add_item_to_menu', return_value=menus.get_test_bad_add_return())
def test_menu_add_db_failure(mock_add):
    resp = TEST_CLIENT.post(f'{ep.MENU_EP}/AnyId', json=menus.get_test_menu())
    assert resp.status_code == SERVICE_UNAVAILABLE
    

@patch('db.menus.del_item_from_menu', autospec=True)
def test_del_menu(mock_delete):
    resp = TEST_CLIENT.delete(f'{ep.MENU_EP}/AnyId')
    assert resp.status_code == OK


@patch('db.menus.del_item_from_menu', side_effect=ValueError, autospec=True)
def test_bad_del_menu(mock_delete):
    resp = TEST_CLIENT.delete(f'{ep.MENU_EP}/AnyId')
    assert resp.status_code == NOT_FOUND


@patch('db.menus.update_price', autospec=True)
def test_update_menu(mock_update):
    resp = TEST_CLIENT.put(f'{ep.MENU_EP}/AnyId', json=menus.get_test_update_menuitem())
    assert resp.status_code == OK


@patch('db.menus.update_price', side_effect=ValueError, autospec=True)
def test_bad_update_menus(mock_update):
    resp = TEST_CLIENT.put(f'{ep.MENU_EP}/AnyId', json=menus.get_test_update_menuitem())
    assert resp.status_code == NOT_FOUND


# Review #
@patch('db.ratings.get_restaurant_ratings', return_value=[], autospec=True)
def test_get_review(mock_get):
    resp = TEST_CLIENT.get(f'{ep.REVIEW_EP}/AnyId')
    assert resp.status_code == OK
    resp_json = resp.get_json()
    assert isinstance(resp_json, dict)


@patch('db.ratings.get_restaurant_ratings', side_effect=ValueError, autospec=True)
def test_bad_get_review(mock_get):
    resp = TEST_CLIENT.get(f'{ep.REVIEW_EP}/AnyId')
    assert resp.status_code == NOT_FOUND


@patch('db.ratings.add_restaurant_rating', return_value=rating.get_test_add_return(), autospec=True)
def test_add_review(mock_add):
    resp = TEST_CLIENT.post(f'{ep.REVIEW_EP}/AnyId', json=rating.get_test_rating())
    assert resp.status_code == OK


@patch('db.ratings.add_restaurant_rating', side_effect=ValueError, autospec=True)
def test_bad_add_review(mock_add):
    resp = TEST_CLIENT.post(f'{ep.REVIEW_EP}/AnyId', json=rating.get_test_rating())
    assert resp.status_code == NOT_ACCEPTABLE


@patch('db.ratings.add_restaurant_rating', return_value=rating.get_test_bad_add_return())
def test_review_add_db_failure(mock_add):
    resp = TEST_CLIENT.post(f'{ep.REVIEW_EP}/AnyId', json=rating.get_test_rating())
    assert resp.status_code == SERVICE_UNAVAILABLE


@patch('db.ratings.del_rating', autospec=True)
def test_del_review(mock_delete):
    resp = TEST_CLIENT.delete(f'{ep.REVIEW_EP}/AnyId')
    assert resp.status_code == OK


@patch('db.ratings.del_rating', side_effect=ValueError, autospec=True)
def test_bad_del_review(mock_delete):
    resp = TEST_CLIENT.delete(f'{ep.REVIEW_EP}/AnyId')
    assert resp.status_code == NOT_FOUND


@patch('db.ratings.update_review_text', autospec=True)
def test_update_review(mock_update):
    resp = TEST_CLIENT.put(f'{ep.REVIEW_EP}/AnyId', json=rating.get_test_update_rating())
    assert resp.status_code == OK


@patch('db.ratings.update_review_text', side_effect=ValueError, autospec=True)
def test_bad_update_review(mock_update):
    resp = TEST_CLIENT.put(f'{ep.REVIEW_EP}/AnyId', json=rating.get_test_update_rating())
    assert resp.status_code == NOT_FOUND


# Category
def test_get_category_name():
    resp = TEST_CLIENT.get(ep.CATEGORY_EP)
    assert resp.status_code == OK
    resp_json = resp.get_json()
    assert isinstance(resp_json, dict)


@patch('db.categories.addCategory', return_value=category.MOCK_ID, autospec=True)
def test_category_add(mock_add):
    """
    Testing we do the right thing with a good return from addCategory.
    """
    resp = TEST_CLIENT.post(ep.CATEGORY_EP, json=category.get_test_category())
    assert resp.status_code == CREATED


@patch('db.categories.addCategory', side_effect=ValueError(), autospec=True)
def test_category_bad_add(mock_add):
    """
    Testing we do the right thing with a value error from addCategory.
    """
    resp = TEST_CLIENT.post(ep.CATEGORY_EP, json=category.get_test_category())
    assert resp.status_code == NOT_ACCEPTABLE


@patch('db.categories.addCategory', return_value=None)
def test_category_add_db_failure(mock_add):
    """
    Testing we do the right thing with a null ID return from addCategory.
    """
    resp = TEST_CLIENT.post(ep.CATEGORY_EP, json=category.get_test_category())
    assert resp.status_code == SERVICE_UNAVAILABLE


@patch('db.categories.deleteCategory', autospec=True)
def test_category_delete(mock_del):
    """
    Testing we do the right thing with a call to deleteCategory that succeeds.
    """
    resp = TEST_CLIENT.delete(f'{ep.CATEGORY_EP}/AnyName')
    assert resp.status_code == OK


@patch('db.categories.deleteCategory', side_effect=ValueError(), autospec=True)
def test_category_bad_delete(mock_del):
    """
    Testing we do the right thing with a value error from deleteCategory.
    """
    resp = TEST_CLIENT.delete(f'{ep.CATEGORY_EP}/AnyName')
    assert resp.status_code == NOT_FOUND
