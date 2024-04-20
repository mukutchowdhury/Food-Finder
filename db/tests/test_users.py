import pytest

import db.users as users

test_obj = {
    users.EMAIL: 'test@test.com',
    users.PASSWORD: 'password',
    users.FNAME: 'test',
    users.LNAME: 'test',
    users.PIMAGE: '',
    users.PRIVILEGE: 0
}


@pytest.fixture(scope='function')
def temp_user():
    users.add_user(test_obj[users.EMAIL], test_obj[users.PASSWORD],
                          test_obj[users.FNAME], test_obj[users.LNAME],
                          test_obj[users.PIMAGE], test_obj[users.PRIVILEGE])  
      
    user_id = users.get_user(test_obj[users.EMAIL], test_obj[users.PASSWORD])

    yield user_id

    if users._id_exists(user_id):
        users.delete_user(user_id)


def test_gen_user_id():
    _id = users._gen_user_id()
    assert isinstance(_id, str)


def test_get_user(temp_user):
    user = users.get_user(test_obj[users.EMAIL], test_obj[users.PASSWORD])
    assert isinstance(user, str)
    assert temp_user == user

def test_get_user_notFound():
    RANDOM_USER = 'RANDOM_USER'
    RANDOM_PASS = 'RANDOM_PASS'
    assert not users._email_exists(RANDOM_USER)
    with pytest.raises(ValueError):
        user = users.get_user(RANDOM_USER, RANDOM_PASS)


def test_get_user_passwordError(temp_user):
    RANDOM_PASS = 'RANDOM_PASS'
    user_data = users.get_userdata(temp_user)
    with pytest.raises(ValueError):
        user = users.get_user(user_data[users.EMAIL], RANDOM_PASS)


def test_get_userdata(temp_user):
    id = temp_user
    user_data = users.get_userdata(id)
    assert isinstance(user_data, dict)
    assert users._id_exists(id)


def test_add_user():
    ret = users.add_user(test_obj[users.EMAIL], test_obj[users.PASSWORD],
                          test_obj[users.FNAME], test_obj[users.LNAME],
                          test_obj[users.PIMAGE], test_obj[users.PRIVILEGE])  
    id = users.get_user(test_obj[users.EMAIL], test_obj[users.PASSWORD])
    assert isinstance(id, str)
    assert users._email_exists(test_obj[users.EMAIL])
    assert isinstance(ret, bool)
    users.delete_user(id)


def test_add_user_dup_email(temp_user):
    with pytest.raises(ValueError):
        ret = users.add_user(test_obj[users.EMAIL], test_obj[users.PASSWORD],
                          test_obj[users.FNAME], test_obj[users.LNAME],
                          test_obj[users.PIMAGE], test_obj[users.PRIVILEGE]) 


def test_del_user(temp_user):
    user_id = temp_user
    users.delete_user(user_id)
    assert not users._id_exists(user_id)


def test_del_user_not_there():
    id = users._gen_user_id()
    with pytest.raises(ValueError):
        users.delete_user(id)
