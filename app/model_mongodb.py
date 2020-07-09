import time

from bson.objectid import ObjectId
from flask_pymongo import PyMongo

builtin_list = list

mongo = None

def _id(id):
    if not isinstance(id, ObjectId):
        return ObjectId(id)
    return id


# [START from_mongo]
def from_mongo(data):
    """
    Translates the MongoDB dictionary format into the format that's expected
    by the application.
    """
    if not data:
        return None

    data['id'] = str(data['_id'])
    return data
# [END from_mongo]


def init_app(app):
    global mongo

    mongo = PyMongo(app)
    mongo.init_app(app)

def count(collection_name):
  return str(mongo.db[collection_name].count())

# [START list]
def list(collection_name, days=7):
  """retrieve the scores within days back."""
  results = mongo.db[collection_name].find({'timestamp': {'$gt': int(time.time()) - 7 * 24 * 3600 * 1000}})
  scores = builtin_list(map(from_mongo, results))
  return scores
# [END list]


# [START create]
def create(collection_name, score):
    result = mongo.db[collection_name].insert_one(score)
# [END create]


def reset(collection_name):
  mongo.db[collection_name].drop()
