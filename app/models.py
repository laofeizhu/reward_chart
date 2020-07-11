import json
import time
import uuid

from app import app


class Badge(object):
    """The badge class"""

    def __init__(self, id=str(uuid.uuid1()), image_url=None, name=None):
        self.id = id
        self.image_url = image_url
        self.name = name


class Prize(Badge):
    """The prize class"""


class Score(object):
    """Score of a child"""

    def __init__(self, timestamp=None, id=str(uuid.uuid1()), point=1, reason=None, badge=None, redeemed=False):
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

    def __init__(self, id=str(uuid.uuid1()), name=None, avatar_url=None, age=None, parents=[], scores=[], birthday=None, prizes=[], current_prize=None):
        self.id = id
        self.name = name
        self.scores = scores
        self.avatar_url = avatar_url
        self.parents = parents
        self.prizes = prizes
        self.current_prize = current_prize

    @classmethod
    def from_json(cls, child_json):
        return Child(**child_json)

class User(object):

    def __init__(self, name=None, username=None, id=str(uuid.uuid1()), password=None, email=None, avatar_url=None, children=[], badges=[]):
        self.name = name
        self.username = username
        self.id = id
        self.password = password
        self.avatar_url = avatar_url
        self.email = email
        self.children = children

        # badges owned by the user
        self.badges = badges

    @classmethod
    def from_json(cls, user_json):
        return User(**user_json)
