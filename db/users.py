import db.db_connect as dbc
import bcrypt
import random

# 1E => Account Exists

BIG_NUM = 1_000_000_000

USER_ID = 'user_id'
EMAIL = 'email'
PASSWORD = 'password'
USERS_COLLECT = 'users'
FNAME = 'fname'
LNAME = 'lname'
PIMAGE = 'pimage'


def exists(email: str) -> bool:
    dbc.connect_db()
    return dbc.fetch_one(USERS_COLLECT, {EMAIL: email})


def _gen_user_id():
    user_id = random.randint(0, BIG_NUM)
    return user_id


def add_user(email: str, password: str, fname: str,
             lname: str, pimage: str = ""):
    if (exists(email)):
        raise ValueError('1B')
    byte_password = password.encode('utf-8')
    hashed_password = bcrypt.hashpw(byte_password, bcrypt.gensalt())
    user_id = _gen_user_id()
    USER = {USER_ID: user_id, EMAIL: email, PASSWORD: hashed_password,
            FNAME: fname, LNAME: lname, PIMAGE: pimage}
    dbc.connect_db()
    _id = dbc.insert_one(USERS_COLLECT, USER)
    return _id is not None


def get_user(email: str, password: str):
    if (exists(email)):
        result = dbc.fetch_one(USERS_COLLECT, {EMAIL: email})
        byte_password = password.encode('utf-8')
        if not bcrypt.checkpw(byte_password, result[PASSWORD]):
            raise ValueError('1C')
        return result[USER_ID]
    else:
        raise ValueError('1A')


def get_userdata(id: int):
    dbc.connect_db()
    result = dbc.fetch_one(USERS_COLLECT, {USER_ID: id})
    return result
