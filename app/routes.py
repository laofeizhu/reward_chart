import json

from datetime import datetime, timedelta

from app import app, socketio, db, models
from flask import render_template, jsonify, request

@app.route('/')
@app.route('/index')
def index():
  username = request.args.get('username')
  if username is None:
    return 'user name must be specified as ?username=xxx'
  return render_template('index.html', username=username)

@app.route('/admin')
def admin():
  username = request.args.get('username')
  if username is None:
    return 'user name must be specified as ?username=xxx'
  return render_template('admin.html', username=username)

def broadcast_star():
  socketio.emit('update star')

@app.route('/_add_star', methods=['GET', 'POST'])
def add_star():
  model = db.get_model()
  username = request.args.get('username')
  if username is None:
    return 'Exception: user name not specified'
  reason = request.args.get('reason')
  if reason is not None:
    app.logger.info('setting reason to ' + reason)
  s = models.Score(username=username, reason=reason)
  model.create(username, s.to_dict())
  broadcast_star()
  return 'Star added'

@app.route('/_reset_star', methods=['POST'])
def reset_star():
  model = db.get_model()
  username = request.args.get('username')
  if username is None:
    return 'Exception: user name not specified'
  model.reset(username)
  broadcast_star()
  return 'Star reset'

@app.route('/_get_stars', methods=['GET'])
def get_star():
  model = db.get_model()
  username = request.args.get('username')
  stars = model.list(username)
  for star in stars:
    star.pop('_id', None)
  return jsonify(stars)
