import time
import uuid


class Score(object):
  """Score of a child"""

  def __init__(self, id=uuid.uuid1(), timestamp=int(time.time()*1000), point=1, reason=None, username=None, redeemed=False):
    self.id = id
    self.timestamp = timestamp
    self.point = point
    self.reason = reason
    self.username = username
    self.redeemed = redeemed

  def to_dict(self):
    return {
        "id": self.id,
        "timestamp": self.timestamp,
        "point": self.point,
        "reason": self.reason,
        "username": self.username,
        "redeemed": self.redeemed
      }
