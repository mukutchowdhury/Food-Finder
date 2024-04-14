import pytest
import db.restaurants as rest

RESTAURANT_ID = 'restaurant_id'
TEST_ZIPCODE = '00000'

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

TEST_RESTAURANT_BLANK = {
    rest.NAME: '',
    rest.ADDRESS: '',
    rest.ZIPCODE: '',
    rest.OWNER_ID: 1,
    rest.IMAGE: '',
    rest.PHONE: 'TEST',
    rest.CUISINE: [],
    rest.KEYWORDS: [],
    rest.CATEGORY: []
}

@pytest.fixture(scope='function')
def temp_restaurant():
    restaurantid = rest.add_restaurant(TEST_RESTAURANT)[RESTAURANT_ID]
    yield restaurantid
    if rest.exists(restaurantid):
        rest.del_restaurant(restaurantid)


def test_get_test_rest_id():
    _id = rest._get_test_rest_id()
    assert isinstance(_id, str)
    assert len(_id) == rest.ID_LEN


def test_get_restuarant(temp_restaurant):
    id = temp_restaurant
    ret = rest.get_restuarant(id)
    assert isinstance(ret, dict)
    assert rest.exists(id)


def test_get_restuarant_NotFound():
    with pytest.raises(ValueError):
        rest.get_restuarant('0')


def test_get_restaurants_by_zipcode():
    ret = rest.get_restaurants_by_zipcode(TEST_ZIPCODE)
    assert isinstance(ret, dict)


def test_add_restaurant():
    ret = rest.add_restaurant(TEST_RESTAURANT)
    assert isinstance(ret, dict)
    assert rest.exists(ret[rest.RESTAURANT_ID])


def test_add_restaurant_Blank():
    with pytest.raises(ValueError):
        rest.add_restaurant(TEST_RESTAURANT_BLANK)


def test_del_restaurant(temp_restaurant):
    id = temp_restaurant
    rest.del_restaurant(id)
    assert not rest.exists(id)


def test_del_restaurant_NotFound():
    with pytest.raises(ValueError):
        rest.del_restaurant('0')


def test_get_all_restaurants():
    all_rests = rest.get_all_restaurants()
    assert isinstance(all_rests, dict)
