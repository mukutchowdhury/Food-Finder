import pytest

import db.db_connect as dbc

TEST_DB = dbc.REST_DB
TEST_COLLECT = 'test_collect'
# can be used for field and value:
TEST_NAME = 'test'
UPDATE = 'Update'


@pytest.fixture(scope='function')
def temp_rec():
    dbc.connect_db()
    dbc.client[TEST_DB][TEST_COLLECT].insert_one({TEST_NAME: TEST_NAME})
    # yield to our test function
    yield
    dbc.client[TEST_DB][TEST_COLLECT].delete_one({TEST_NAME: TEST_NAME})


def test_fetch_one(temp_rec):
    ret = dbc.fetch_one(TEST_COLLECT, {TEST_NAME: TEST_NAME})
    assert ret is not None


def test_fetch_one_not_there(temp_rec):
    ret = dbc.fetch_one(TEST_COLLECT, {TEST_NAME: 'not a field value in db!'})
    assert ret is None


def test_up_one(temp_rec):
    # Assuming dbc is an instance of your database client
    dbc.up_one(TEST_COLLECT, {TEST_NAME: TEST_NAME}, {'$set': {TEST_NAME: UPDATE}})
    ret = dbc.fetch_one(TEST_COLLECT, {TEST_NAME: UPDATE})
    assert ret is not None
    dbc.del_one(TEST_COLLECT, {TEST_NAME: UPDATE})


def test_fetch_all(temp_rec):
    ret = dbc.fetch_all(TEST_COLLECT)
    assert ret is not None
