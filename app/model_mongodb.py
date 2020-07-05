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


# [START list]
def list(dbname):
  results = mongo.db[dbname].find()
  scores = builtin_list(map(from_mongo, results))
  return scores
# [END list]


# [START create]
def create(dbname, score):
    result = mongo.db[dbname].insert_one(score)
# [END create]


def reset(dbname):
  mongo.db[dbname].drop()