import json

from datetime import datetime, timedelta

from app import app, models, socketio, db
from flask import render_template, jsonify, request

@app.route('/')
@app.route('/index')
def index():
  username = request.args.get('username')
  if username is None:
    return 'user name must be specified as /username=xxx'
  return render_template('index.html', username=username)

@app.route('/admin')
def admin():
  username = request.args.get('username')
  if username is None:
    return 'user name must be specified as /username=xxx'
  return render_template('admin.html', username=username)

def broadcast_star():
  socketio.emit('update star')

@app.route('/_add_star', methods=['GET', 'POST'])
def add_star():
  s = models.Score()
  username = request.args.get('username')
  if username is None:
    return 'Exception: user name not specified'
  s.username=username
  reason = request.args.get('reason')
  if reason is not None:
    app.logger.info('setting reason to ' + reason)
    s.reason = reason
  db.session.add(s)
  db.session.commit()

  broadcast_star()
  return 'Star added'

@app.route('/_reset_star', methods=['POST'])
def reset_star():
  models.Score.query.filter(models.Score.username==username).delete()
  # add two stars for yesterday and tomorrow for debugging purpose
  # now = datetime.utcnow()
  # one_day = timedelta(days=1)
  # s = models.Score(timestamp=(now+one_day))
  # db.session.add(s)
  # s = models.Score(timestamp=(now-one_day))
  # db.session.add(s)
  db.session.commit()
  broadcast_star()
  return 'Star reset'

@app.route('/_get_stars', methods=['GET'])
def get_star():
  stars = []
  username = request.args.get('username')
  for entry in models.Score.query.filter(models.Score.username==username).all():
    star = {}
    star['point'] = entry.point
    star['id'] = entry.id
    star['timestamp'] = int(datetime.timestamp(entry.timestamp) * 1000)
    star['reason'] = entry.reason
    stars.append(star)
  return jsonify(stars)
