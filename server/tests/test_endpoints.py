from http.client import (BAD_REQUEST, FORBIDDEN, NOT_ACCEPTABLE, NOT_FOUND, OK,
                         SERVICE_UNAVAILABLE)
from unittest.mock import patch

import pytest

import db.menus as menus
import db.ratings as rating
import db.options as options
import db.restaurants as rest
import server.endpoints as ep

TEST_CLIENT = ep.app.test_client()

def test_hello():
    resp = TEST_CLIENT.get(ep.HELLO_EP)
    print(f'{resp=}')
    resp_json = resp.get_json()
    print(f'{resp_json=}')
    assert ep.HELLO_RESP in resp_json

# Restaurants #
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


@patch('db.restaurants.get_restaurants', side_effect=None, autospec=True)
def test_get_all_restaurant(mock_get):
    resp = TEST_CLIENT.get(f'{ep.RestaurantEP}/123')
    assert resp.status_code == NOT_FOUND
    # resp_json = resp.get_json()
    # assert isinstance(resp_json, dict)

# Menus #
@patch('db.menus.get_restuarant_menu', return_value=None, autospec=True)
def test_get_menu(mock_get):
    resp = TEST_CLIENT.get(f'{ep.Menu_EP}/123')
    assert resp.status_code == OK


@patch('db.menus.get_restuarant_menu', side_effect=ValueError, autospec=True)
def test_bad_get_menu(mock_get):
    resp = TEST_CLIENT.get(f'{ep.Menu_EP}/123')
    assert resp.status_code == NOT_FOUND


@patch('db.menus.add_item_to_menu', return_value=rest.MOCK_ID, autospec=True)
def test_add_menu(mock_add):
    resp = TEST_CLIENT.post(f'{ep.Menu_EP}/123', json=menus.get_test_menu())
    assert resp.status_code == OK


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


@patch('db.menus.add_item_to_menu', return_value=None)
def test_menu_add_db_failure(mock_add):
    resp = TEST_CLIENT.post(f'{ep.Menu_EP}/123', json=menus.get_test_menu())
    assert resp.status_code == SERVICE_UNAVAILABLE
    

@patch('db.menus.del_item_from_menu', return_value=None, autospec=True)
def test_del_menu(mock_delete):
    resp = TEST_CLIENT.delete(f'{ep.Menu_EP}/123')
    assert resp.status_code == OK


@patch('db.menus.del_item_from_menu', side_effect=ValueError, autospec=True)
def test_bad_del_menu(mock_delete):
    resp = TEST_CLIENT.delete(f'{ep.Menu_EP}/123')
    assert resp.status_code == NOT_FOUND


@patch('db.menus.update_item_price', return_value=None, autospec=True)
def test_update_menu(mock_update):
    resp = TEST_CLIENT.put(f'{ep.Menu_EP}/123', json={'new_price': 1.59})
    assert resp.status_code == OK

    """
    resp = TEST_CLIENT.post(ep.Restaurant_EP, json=rest.del_restaurant)
    assert resp.status_code == OK or 500
    """

@pytest.mark.skip('skip this test, come back to it later')
@patch('db.restaurants.add_restaurant', side_effect=None, autospec=True)
def test_register_add_restaurant(mock_add):
    """
    Testing with a restaurant entry

    """
    resp = TEST_CLIENT.post(ep.Add_Restaurant, json=rest.get_test_restaurant)
    assert resp.status_code == OK

@patch('db.menus.update_item_price', side_effect=ValueError, autospec=True)
def test_bad_update_menus(mock_update):
    resp = TEST_CLIENT.put(f'{ep.Menu_EP}/123', json={'new_price': 1.59})
    assert resp.status_code == NOT_FOUND

# Review #
@patch('db.ratings.get_all_ratings', return_value=None, autospec=True)
def test_get_review(mock_get):
    resp = TEST_CLIENT.get(f'{ep.REVIEW_EP}/123')
    assert resp.status_code == OK


@patch('db.ratings.get_all_ratings', side_effect=ValueError, autospec=True)
def test_bad_get_review(mock_get):
    resp = TEST_CLIENT.get(f'{ep.REVIEW_EP}/123')
    assert resp.status_code == NOT_FOUND


@patch('db.ratings.add_restaurant_rating', return_value=rest.MOCK_ID, autospec=True)
def test_add_review(mock_add):
    resp = TEST_CLIENT.post(f'{ep.REVIEW_EP}/123', json=rating.get_test_rating())
    assert resp.status_code == OK


@patch('db.ratings.add_restaurant_rating', side_effect=ValueError, autospec=True)
def test_bad_add_review(mock_add):
    resp = TEST_CLIENT.post(f'{ep.REVIEW_EP}/123', json=rating.get_test_rating())
    assert resp.status_code == NOT_ACCEPTABLE


@patch('db.ratings.add_restaurant_rating', return_value=None)
def test_review_add_db_failure(mock_add):
    resp = TEST_CLIENT.post(f'{ep.REVIEW_EP}/123', json=rating.get_test_rating())
    assert resp.status_code == SERVICE_UNAVAILABLE


@patch('db.ratings.del_rating', return_value=None, autospec=True)
def test_del_review(mock_delete):
    resp = TEST_CLIENT.delete(f'{ep.REVIEW_EP}/123')
    assert resp.status_code == OK


@patch('db.ratings.del_rating', side_effect=ValueError, autospec=True)
def test_bad_del_review(mock_delete):
    resp = TEST_CLIENT.delete(f'{ep.REVIEW_EP}/123')
    assert resp.status_code == NOT_FOUND


@patch('db.ratings.update_review_text', return_value=None, autospec=True)
def test_update_review(mock_update):
    resp = TEST_CLIENT.put(f'{ep.REVIEW_EP}/123', json={'text': 'Hello Text'})
    assert resp.status_code == OK


@patch('db.ratings.update_review_text', side_effect=ValueError, autospec=True)
def test_bad_update_review(mock_update):
    resp = TEST_CLIENT.put(f'{ep.REVIEW_EP}/123', json={'text': 'Hello Text'})
    assert resp.status_code == NOT_FOUND


# Hours #
@patch('db.options.get_restaurant_hour', return_value=None, autospec=True)
def test_get_rhour(mock_get):
    resp = TEST_CLIENT.get(f'{ep.HOUR_EP}/123')
    assert resp.status_code == OK


@patch('db.options.get_restaurant_hour', side_effect=ValueError, autospec=True)
def test_bad_get_hour(mock_get):
    resp = TEST_CLIENT.get(f'{ep.HOUR_EP}/123')
    assert resp.status_code == NOT_FOUND


@patch('db.options.insert_restaurant_hour', return_value=rest.MOCK_ID, autospec=True)
def test_add_hour(mock_add):
    resp = TEST_CLIENT.post(f'{ep.HOUR_EP}/123', json=options.get_test_hour())
    assert resp.status_code == OK


@patch('db.options.insert_restaurant_hour', side_effect=ValueError, autospec=True)
def test_bad_add_hour(mock_add):
    resp = TEST_CLIENT.post(f'{ep.HOUR_EP}/123', json=options.get_test_hour())
    assert resp.status_code == NOT_ACCEPTABLE


@patch('db.options.insert_restaurant_hour', return_value=None)
def test_hour_add_db_failure(mock_add):
    resp = TEST_CLIENT.post(f'{ep.HOUR_EP}/123', json=options.get_test_hour())
    assert resp.status_code == SERVICE_UNAVAILABLE


@patch('db.options.delete_restaurant_time', return_value=None, autospec=True)
def test_del_hour(mock_delete):
    resp = TEST_CLIENT.delete(f'{ep.HOUR_EP}/123')
    assert resp.status_code == OK


@patch('db.options.delete_restaurant_time', side_effect=ValueError, autospec=True)
def test_bad_del_hour(mock_delete):
    resp = TEST_CLIENT.delete(f'{ep.HOUR_EP}/123')
    assert resp.status_code == NOT_FOUND


@patch('db.options.update_restaurant_time', return_value=None, autospec=True)
def test_update_hour(mock_update):
    resp = TEST_CLIENT.put(f'{ep.HOUR_EP}/123', json=options.get_test_hour())
    assert resp.status_code == OK


@patch('db.options.update_restaurant_time', side_effect=ValueError, autospec=True)
def test_bad_update_hour(mock_update):
    resp = TEST_CLIENT.put(f'{ep.HOUR_EP}/123', json=options.get_test_hour())
    assert resp.status_code == NOT_FOUND