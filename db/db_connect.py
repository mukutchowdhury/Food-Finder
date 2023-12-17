import os

import pymongo as pm

LOCAL = "0"
CLOUD = "1"

REST_DB = 'restaurantDB'
client = None

MONGO_ID = '_id'


def connect_db():
    """
    This provides a uniform way to connect to the DB across all uses.
    Returns a mongo client object... maybe we shouldn't?
    Also set global client variable.
    We should probably either return a client OR set a
    client global.
    """
    global client
    if client is None:  # not connected yet!
        print("Setting client because it is None.")
        if os.environ.get("CLOUD_MONGO", LOCAL) == CLOUD:
            password = os.environ.get("MONGODB_PASSWORD")
            if not password:
                raise ValueError('You must set your password '
                                 + 'to use Mongo in the cloud.')
            print("Connecting to Mongo in the cloud.")
            client = pm.MongoClient(f'mongodb+srv://jw6680:{password}'
                                    + '@food-finder.ltqe7ym.mongodb.net/'
                                    + '{REST_DB}?retryWrites=true&w=majority')
            # PA recommends these settings:
            # + 'connectTimeoutMS=30000&'
            # + 'socketTimeoutMS=None
            # + '&connect=false'
            # + 'maxPoolsize=1')
            # but they don't seem necessary
        else:
            print("Connecting to Mongo locally.")
            client = pm.MongoClient()


def insert_one(collection, doc, db=REST_DB):
    """
    Insert a single doc into collection.
    """
    print(f'{db=}')
    return client[db][collection].insert_one(doc)


def fetch_one(collection, filt, db=REST_DB):
    """
    Find with a filter and return on the first doc found.
    """
    for doc in client[db][collection].find(filt):
        if MONGO_ID in doc:
            # Convert mongo ID to a string so it works as JSON
            doc[MONGO_ID] = str(doc[MONGO_ID])
        return doc


def fetch_all_by_key(collection, filt, db=REST_DB):
    """
    Find with a filter and return all docs matching the filter.
    """
    result = []
    for doc in client[db][collection].find(filt):
        if MONGO_ID in doc:
            # Convert mongo ID to a string so it works as JSON
            doc[MONGO_ID] = str(doc[MONGO_ID])
        result.append(doc)
    return result


def del_one(collection, filt, db=REST_DB):
    """
    Find with a filter and return on the first doc found.
    """
    client[db][collection].delete_one(filt)


def fetch_all(collection, db=REST_DB):
    ret = []
    for doc in client[db][collection].find():
        ret.append(doc)
    return ret


def fetch_all_as_dict(key, collection, db=REST_DB):
    ret = {}
    for doc in client[db][collection].find():
        del doc[MONGO_ID]
        ret[doc[key]] = doc
    return ret


def up_one(collection, filt, update, db=REST_DB):
    client[db][collection].update_one(filt, update)


def update_doc(collection, filters, update_dict, db=REST_DB):
    return client[db][collection].update_one(filters, {'$set': update_dict})
