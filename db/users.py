import db.db_connect as dbc
import bcrypt
import random

# 1E => Account Exists
# 1C => Password Do Not Match
# 1A => Get Email Not Found
# 1D => Delete Id Not Found
# 1B => Add Email Exists

ID_LEN = 24
BIG_NUM = 100_000_000_000_000_000_000

MOCK_ID = '0' * ID_LEN

USER_ID = 'user_id'
EMAIL = 'email'
PASSWORD = 'password'
USERS_COLLECT = 'users'
FNAME = 'fname'
LNAME = 'lname'
PIMAGE = 'pimage'
PRIVILEGE = 'privilege'


def get_test_user():
    test_user = {}
    test_user[EMAIL] = 'TEST'
    test_user[PASSWORD] = 'TEST'
    test_user[FNAME] = 'TEST'
    test_user[LNAME] = 'TEST'
    test_user[PIMAGE] = ''
    test_user[PRIVILEGE] = '0'
    return test_user


def get_test_login_user():
    test_user = {}
    test_user[EMAIL] = 'TEST'
    test_user[PASSWORD] = 'TEST'
    return test_user


def _email_exists(email: str) -> bool:
    dbc.connect_db()
    return dbc.fetch_one(USERS_COLLECT, {EMAIL: email})


def _id_exists(id: str) -> bool:
    dbc.connect_db()
    return dbc.fetch_one(USERS_COLLECT, {USER_ID: id})


def _gen_user_id() -> str:
    _id = random.randint(0, BIG_NUM)
    _id = str(_id)
    _id = _id.rjust(ID_LEN, '0')
    return _id


def add_user(email: str, password: str, fname: str,
             lname: str, pimage: str = "", privilege: int = 0):
    if (_email_exists(email)):
        raise ValueError('1B')
    byte_password = password.encode('utf-8')
    hashed_password = bcrypt.hashpw(byte_password, bcrypt.gensalt())
    user_id = _gen_user_id()
    USER = {USER_ID: user_id, EMAIL: email, PASSWORD: hashed_password,
            FNAME: fname, LNAME: lname, PIMAGE: pimage, PRIVILEGE: privilege}
    dbc.connect_db()
    _id = dbc.insert_one(USERS_COLLECT, USER)
    return _id is not None


def get_user(email: str, password: str):
    if (_email_exists(email)):
        result = dbc.fetch_one(USERS_COLLECT, {EMAIL: email})
        byte_password = password.encode('utf-8')
        if not bcrypt.checkpw(byte_password, result[PASSWORD]):
            raise ValueError('1C')
        return result[USER_ID]
    else:
        raise ValueError('1A')


def get_userdata(id: str):
    dbc.connect_db()
    if (_id_exists(id)):
        return dbc.fetch_one_as_dict(USERS_COLLECT, {USER_ID: id})
    raise ValueError('1D')


def delete_user(id: str):
    if (_id_exists(id)):
        return dbc.del_one(USERS_COLLECT, {USER_ID: id})
    raise ValueError('1D')
