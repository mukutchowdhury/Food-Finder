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
    rest.CATEGORY: [],
    rest.HOURS: {
        rest.OPEN: '12:00PM',
        rest.CLOSE: '12:00AM',
    }
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
    rest.CATEGORY: [],
    rest.HOURS: {
        rest.OPEN: '',
        rest.CLOSE: '',
    }
}

TEST_OPEN = '11:00AM'
TEST_CLOSE = '11:00PM'

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


def test_get_restaurant(temp_restaurant):
    id = temp_restaurant
    ret = rest.get_restaurant(id)
    assert isinstance(ret, dict)
    assert rest.exists(id)


def test_get_restaurant_NotFound():
    with pytest.raises(ValueError):
        rest.get_restaurant('0')


def test_get_restaurants_by_zipcode():
    ret = rest.get_restaurants_by_zipcode(TEST_ZIPCODE)
    assert isinstance(ret, dict)


def test_add_restaurant():
    ret = rest.add_restaurant(TEST_RESTAURANT)
    assert isinstance(ret, dict)
    assert rest.exists(ret[rest.RESTAURANT_ID])
    rest.del_restaurant(ret[rest.RESTAURANT_ID])


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


def test_update_restaurant_time(temp_restaurant):
    rest_id = temp_restaurant
    rest.update_restaurant_time(temp_restaurant, TEST_OPEN, TEST_CLOSE)
    assert rest.exists(rest_id)


def test_update_restaurant_time_NotFound():
    with pytest.raises(ValueError):
        rest.update_restaurant_time('0', TEST_OPEN, TEST_CLOSE)


def test_get_test_restaurant():
    restaurant = rest.get_test_restaurant()
    assert (rest.NAME in restaurant)
    assert (rest.ADDRESS in restaurant)
    assert (rest.ZIPCODE in restaurant)
    assert (rest.OWNER_ID in restaurant)
    assert (rest.IMAGE in restaurant)
    assert (rest.PHONE in restaurant)
    assert (rest.CUISINE in restaurant)
    assert (rest.KEYWORDS in restaurant)
    assert (rest.CATEGORY in restaurant)
    assert (rest.HOURS in restaurant)


def test_get_test_add_return():
    add_return = rest.get_test_add_return()
    assert (rest.STATUS in add_return)
    assert (rest.RESTAURANT_ID in add_return)


def test_get_test_bad_add_return():
    bad_add_return = rest.get_test_bad_add_return()
    assert (rest.STATUS in bad_add_return)
    assert (rest.RESTAURANT_ID in bad_add_return)


def test_get_test_update_hour():
    update_hour = rest.get_test_update_hour()
    assert (rest.OPEN in update_hour)
    assert (rest.CLOSE in update_hour)
