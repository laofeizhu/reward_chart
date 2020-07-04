from app import db
from datetime import datetime
import uuid


class Score(db.Model):
  id = db.Column(db.String, primary_key=True, default=lambda: str(uuid.uuid1()), unique=True, nullable=False)
  point = db.Column(db.Integer, index=True, default=1)
  timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
  reason = db.Column(db.String, index=True)
  username = db.Column(db.String, index=True)


  def __repr__(self):
    return '<Score User={} ID={} Point={} for ({}) @ {}>'.format(self.username, self.id, self.point, self.reason, self.timestamp)
    
