import json
import time
import uuid

class JSONEncoder(json.JSONEncoder):

  def default(self, obj):
    if hasattr(obj, 'to_json'):
      return obj.to_json()
    else:
      return json.JSONEncoder.default(self, obj)


class Badge(object):
  """The badge class"""

  def __init__(self, image_url=None, name=None):
    self.image_url = image_url
    self.name = name
  
  def to_json(self):
    return dict(image_url=self.image_url, name=self.name)


class Prize(Badge):
  """The prize class"""


class Score(object):
  """Score of a child"""

  def __init__(self, timestamp=None, point=1, reason=None, badge=None, redeemed=False):
    self.timestamp = timestamp
    self.point = point
    self.reason = reason
    self.badge = badge
    self.redeemed = redeemed

  def to_json(self):
    return dict(timestamp=self.timestamp, point=self.point, reason=self.reason, badge=self.badge, redeemed=self.redeemed)


class Timestamp(object):

  def __init__(self, seconds=seconds, nanos=nanos):
    self.seconds = seconds
    self.nanos = nanos

  def to_json(self):
    return dict(seconds=self.seconds, nanos=self.nanos)


class Child(object):
  """The child class"""

  def __init__(self, id=None, name=None, age=None, parents=[], scores=[], birthday=None, prizes=[], current_prize=None):
    self.id = id
    self.name = name
    self.age = age
    self.scores = scores
    self.parents = parents
    self.birthday = birthday
    self.prizes = prizes
    self.current_prize = current_prize



class User(object):

  def __init__(self, name=None, id=None, password=None, avatar=None, children=[], badges=[]):
    self.Name = name
    self.id = id
    self.password = password
    self.avatar = avatar
    self.children = children
    self.badges = badges