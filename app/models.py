import json
import time
import uuid

from app import app


class Badge(object):
    """The badge class"""

    def __init__(self, id=None, image_url=None, name=None):
        self.id = id if id is not None else str(uuid.uuid1())
        self.image_url = image_url
        self.name = name

    @classmethod
    def from_json(cls, badge_json):
        return Badge(**badge_json)


class Reward(object):
    """The reward class"""

    def __init__(self, id=None, image_url=None, name=None, score=None):
        self.id = id if id is not None else str(uuid.uuid1())
        self.image_url = image_url
        self.name = name
        # score needed for this reward
        self.score = score

    
    @classmethod
    def from_json(cls, reward_json):
        return Reward(**reward_json)



class Score(object):
    """Score of a child"""

    def __init__(self, timestamp=None, id=None, point=1, reason=None, badge=None, redeemed=False):
        # timestamp is in utc sec
        self.timestamp = timestamp
        self.point = point
        self.id = id if id is not None else str(uuid.uuid1())
        self.reason = reason
        self.badge = badge
        self.redeemed = redeemed

    
    @classmethod
    def from_json(cls, score_json):
        return Score(**score_json)

class Child(object):
    """The child class"""

    def __init__(self, id=None, name=None, avatar_url=None, age=None, parents=[], scores=[], birthday=None, rewards=[], current_reward=None):
        self.id = id if id is not None else str(uuid.uuid1())
        self.name = name
        self.scores = scores
        self.avatar_url = avatar_url
        self.parents = parents
        self.rewards = rewards
        self.current_reward = current_reward

    @classmethod
    def from_json(cls, child_json):
        return Child(**child_json)

class User(object):

    def __init__(self, name=None, username=None, id=None, password=None, email=None, rewards=[], avatar_url=None, children=[], badges=[]):
        self.name = name
        self.username = username
        self.id = id if id is not None else str(uuid.uuid1())
        self.password = password
        self.avatar_url = avatar_url
        self.email = email
        self.children = children
        self.rewards = rewards

        # badges owned by the user
        self.badges = badges

    @classmethod
    def from_json(cls, user_json):
        return User(**user_json)
