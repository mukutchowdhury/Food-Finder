import db.db_connect as dbc
import random

CATEGORY_COLLECTION = 'categories'
NAME = 'name'
DESCRIPTION = 'description'

ID_LEN = 24
BIG_NUM = 100_000_000_000_000_000_000

MOCK_ID = '0' * ID_LEN


def _get_test_name():
    name = 'test'
    rand_part = random.randint(0, BIG_NUM)
    return name + str(rand_part)


def get_test_category():
    test_category = {}
    test_category[NAME] = _get_test_name()
    test_category[DESCRIPTION] = ''
    return test_category


def addCategory(name: str, descpription: str = ""):
    if (exists(name)):
        raise ValueError(f'Category name exists, {name}')
    CATEGORY = {NAME: name, DESCRIPTION: descpription}
    dbc.connect_db()
    _id = dbc.insert_one(CATEGORY_COLLECTION, CATEGORY)
    return _id is not None


def getCategories():
    dbc.connect_db()
    return dbc.fetch_all_as_dict(NAME, CATEGORY_COLLECTION)


def exists(name: str) -> bool:
    dbc.connect_db()
    return dbc.fetch_one(CATEGORY_COLLECTION, {NAME: name})


def deleteCategory(name: str):
    if exists(name):
        return dbc.del_one(CATEGORY_COLLECTION, {NAME: name})
    raise ValueError(f'Delete failure: {name} not found.')
