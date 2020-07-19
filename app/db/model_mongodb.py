import time
import ssl

from bson.objectid import ObjectId
from flask_pymongo import PyMongo
from app import models, app

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

    data.pop('_id')
    return data
# [END from_mongo]


def init_app(app):
    global mongo

    mongo = PyMongo(app, ssl_cert_reqs=ssl.CERT_NONE)
    mongo.init_app(app)

def send_file(filename):
  return mongo.send_file(filename)

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

def save_file(filename, file):
  mongo.save_file(filename, file)


def register_user(user):
  app.logger.info('adding user {} to db'.format(user))
  mongo.db['users'].insert_one(user.__dict__)



def get_user(username_or_email=None, id=None):
  if id is not None:
    results = mongo.db['users'].find({'id': id})
  elif '@' in username_or_email:
    results = mongo.db['users'].find({'email': username_or_email})
  else:
    results = mongo.db['users'].find({'username': username_or_email})
  users_json = builtin_list(map(from_mongo, results))
  return None if len(users_json) == 0 else models.User.from_json(users_json[0])

def register_child(child):
  mongo.db['children'].insert_one(child.__dict__)


def add_child(user_id=None, child_id=None):
  mongo.db['users'].update({'id': user_id}, {'$push': {'children': child_id}})
  mongo.db['children'].update({'id': child_id}, {'$push': {'parents': user_id}})

def get_child(id=None):
  results = mongo.db['children'].find({'id': id})
  child_json = builtin_list(map(from_mongo, results))
  return None if len(child_json) == 0 else models.Child.from_json(child_json[0])

def get_child_score_count(id=None):
  results = mongo.db['children'].find({'id': id})
  return len(results[0]['scores'])

def add_reward_to_user(user_id=None, reward_id=None):
  app.logger.info('adding reward {} to user {}'.format(reward_id, user_id))
  mongo.db['users'].update({'id': user_id}, {'$push': {'rewards': reward_id}})


def register_reward(reward):
  mongo.db['rewards'].insert_one(reward.__dict__)

def get_reward(id=None):
  results = mongo.db['rewards'].find({'id': id})
  reward_json = builtin_list(map(from_mongo, results))
  return None if len(reward_json) == 0 else models.Reward.from_json(reward_json[0])


def register_badge(badge):
  mongo.db['badges'].insert_one(badge.__dict__)

def get_badge(id=None):
  results = mongo.db['badges'].find({'id': id})
  badge_json = builtin_list(map(from_mongo, results))
  return None if len(badge_json) == 0 else models.Badge.from_json(badge_json[0])

def add_badge_to_user(user_id=None, badge_id=None):
  app.logger.info('adding badge {} to user {}'.format(badge_id, user_id))
  mongo.db['users'].update({'id': user_id}, {'$push': {'badges': badge_id}})


def add_score(score=None, child_id=None):
  mongo.db['scores'].insert_one(score.__dict__)
  mongo.db['children'].update(
    {'id': child_id},
    {
      '$push': {'scores': score.id},
      '$inc': {'score_balance': 1}
    },
  )


def get_score(id=None):
  results = mongo.db['scores'].find({'id': id})
  score_json = builtin_list(map(from_mongo, results))
  return None if len(score_json) == 0 else models.Score.from_json(score_json[0])

def delete_score(score_id=None, child_id=None):
  mongo.db['scores'].delete_one({'id': score_id})
  if child_id is not None:
    mongo.db['children'].update(
      {
        'id': child_id
      },
      {
      '$pull': {
        'scores': score_id
      },
      '$inc': {'score_balance': -1}
    })

def delete_child(child_id=None, user_id=None):
  mongo.db['users'].update(
    {
      'id': user_id
    },
    {
      '$pull': {
        'children': child_id
      }
    }
  )
  child = get_child(child_id)
  if len(child.parents) != 1:
    mongo.db['children'].update(
      {
        'id': child_id
      },
      {
        '$pull': {
          'parents': user_id
        }
      }
    )
  else:
    # remove this orphan and their scores
    for score_id in child.scores:
      delete_score(score_id, child_id)
  mongo.db['children'].delete_one({'id': child_id})
    
  