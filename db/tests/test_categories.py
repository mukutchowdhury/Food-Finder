import pytest

import db.categories as cat

TEST_NAME = 'test_name'
TEST_DESCRIPTION = 'test_description'


@pytest.fixture(scope='function')
def temp_category():
    ret = cat.addCategory(TEST_NAME, TEST_DESCRIPTION)
    yield TEST_NAME
    if cat.exists(TEST_NAME):
        cat.deleteCategory(TEST_NAME)


def test_addCategory():
    ret = cat.addCategory(TEST_NAME, TEST_DESCRIPTION)
    assert cat.exists(TEST_NAME)
    assert isinstance(ret, bool)
    cat.deleteCategory(TEST_NAME)


def test_addCategory_duplicate(temp_category):
    with pytest.raises(ValueError):
        cat.addCategory(temp_category, TEST_DESCRIPTION)


def test_getCategories(temp_category):
    categories = cat.getCategories()
    assert isinstance(categories, dict)
    for category in categories:
        assert isinstance(category, str)
        assert isinstance(categories[category], dict)
    assert cat.exists(temp_category)


def test_deleteCategory(temp_category):
    categoryName = temp_category
    cat.deleteCategory(categoryName)
    assert not cat.exists(categoryName)


def test_deleteCategory_NotFound():
    with pytest.raises(ValueError):
        cat.deleteCategory(TEST_NAME)


def test__get_test_name():
    test_name = cat._get_test_name()
    assert isinstance(test_name, str)


def test_get_test_category():
    category = cat.get_test_category()
    assert cat.NAME in category
    assert cat.DESCRIPTION in category
