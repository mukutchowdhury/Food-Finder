import db.db_connect as dbc

# Variables
RESTAURANT_ID = 'restaurant_id'
OPEN_TIME = 'open_time'
CLOSE_TIME = 'close_time'


# Mongodb Collection
OPTIONS_COLLECT = 'options'
REST_COLLECT = 'restaurants'


def hour_exist(restaurant_id: int) -> bool:
    dbc.connect_db()
    return dbc.fetch_one(OPTIONS_COLLECT, {RESTAURANT_ID: restaurant_id})


def restaurant_exist(restaurant_id: int) -> bool:
    dbc.connect_db()
    return dbc.fetch_one(REST_COLLECT, {RESTAURANT_ID: restaurant_id})


def get_restaurant_hour(restaurant_id: int) -> dict:
    if hour_exist(restaurant_id):
        return dbc.fetch_one(OPTIONS_COLLECT, {RESTAURANT_ID: restaurant_id})
    raise ValueError(f'GET failure: {restaurant_id} does not have a set hour.')


def _adjust_time(time: dict) -> str:
    hour = max(0, min(23, time['hour']))
    minute = max(0, min(59, time['minute']))
    return f'{hour}:{minute}'


def insert_restaurant_hour(restaurant_id: int,
                           open: dict, close: dict) -> int:
    if not restaurant_exist(restaurant_id):
        raise ValueError('POST failure: ' +
                         f'{restaurant_id} is not a restaurant.')
    if hour_exist(restaurant_id):
        raise ValueError('POST failure: ' +
                         f'{restaurant_id} already has a set hour')

    open_time = _adjust_time(open)
    close_time = _adjust_time(close)

    hour = {RESTAURANT_ID: restaurant_id,
            OPEN_TIME: open_time,
            CLOSE_TIME: close_time}

    dbc.connect_db()
    _id = dbc.insert_one(OPTIONS_COLLECT, hour)

    return _id is not None


def update_restaurant_time(restaurant_id: int,
                           open: dict, close: dict):
    if hour_exist(restaurant_id):
        open_time = _adjust_time(open)
        close_time = _adjust_time(close)

        return dbc.up_one(
            OPTIONS_COLLECT,
            {RESTAURANT_ID: restaurant_id},
            {"$set": {OPEN_TIME: open_time, CLOSE_TIME: close_time}}
        )
    raise ValueError('PUT failure: ' +
                     f'{restaurant_id} has no existing time')


def delete_restaurant_time(restaurant_id: int):
    if hour_exist(restaurant_id):
        return dbc.del_one(OPTIONS_COLLECT, {RESTAURANT_ID: restaurant_id})
    raise ValueError('DELETE failure: ' +
                     f'{restaurant_id} has no existing time')
