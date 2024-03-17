import db.db_connect as dbc

CATEGORY_COLLECTION = 'categories'
NAME = 'name'
DESCRIPTION = 'description'


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


def delete_category(name: str):
    if exists(name):
        return dbc.del_one(CATEGORY_COLLECTION, {NAME: name})
    raise ValueError(f'Delete failure: {name} not found.')
