import json
import time
import uuid

from app import app


class Badge(object):
  """The badge class"""

  def __init__(self, image_url=None, name=None):
    self.image_url = image_url
    self.name = name


class Prize(Badge):
  """The prize class"""


class Score(object):
  """Score of a child"""

  def __init__(self, timestamp=None, id=None, point=1, reason=None, badge=None, redeemed=False):
    self.timestamp = timestamp
    self.point = point
    self.id = id
    self.reason = reason
    self.badge = badge
    self.redeemed = redeemed


class Timestamp(object):

  def __init__(self, seconds=0, nanos=0):
    self.seconds = seconds
    self.nanos = nanos


class Child(object):
  """The child class"""

  def __init__(self, id=None, name=None, age=None, parents=[], scores=[], birthday=None, prizes=[], current_prize=None):
    self.id = str(uuid.uuid1())
    self.name = name
    self.scores = scores
    self.avatar_url = avatar_url
    self.parents = parents
    self.prizes = prizes
    self.current_prize = current_prize


class User(object):

  def __init__(self, name=None, username=None, id=None, password=None, email=None, avatar_url=None, children_ids=[], badges=[]):
    self.name = name
    self.username = username
    self.id = str(uuid.uuid1())
    self.password = password
    self.avatar_url = avatar_url
    self.email = email
    self.children_ids = children_ids

    # badges owned by the user
    self.badges = badges

  @classmethod
  def from_json(cls, user_json):
    return User(**user_json)
