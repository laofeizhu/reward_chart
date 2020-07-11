import json

from datetime import datetime, timedelta

from app import app, db, models
from app.forms import LoginForm
from flask import render_template, jsonify, request, url_for, flash, redirect

@app.route('/')
@app.route('/index')
def index():
  return render_template('index.html')

@app.route('/admin')
def admin():
  username = request.args.get('username')
  if username is None:
    return 'user name must be specified as ?username=xxx'
  return render_template('admin.html', username=username)

@app.route('/_add_star', methods=['GET', 'POST'])
def add_star():
  model = db.get_model()
  username = request.args.get('username')
  if username is None:
    return 'Exception: user name not specified'
  reason = request.args.get('reason')
  if reason is not None:
    app.logger.info('setting reason to ' + reason)
  timestamp = request.args.get('timestamp')
  s = models.Score(username=username, reason=reason, timestamp=int(timestamp))
  model.create(username, s.to_dict())
  return 'Star added'

@app.route('/_reset_star', methods=['POST'])
def reset_star():
  model = db.get_model()
  username = request.args.get('username')
  if username is None:
    return 'Exception: user name not specified'
  model.reset(username)
  return 'Star reset'

@app.route('/_get_stars', methods=['GET'])
def get_star():
  model = db.get_model()
  username = request.args.get('username')
  stars = model.list(username)
  for star in stars:
    star.pop('_id', None)
  return jsonify(stars)

@app.route('/_get_stars_count', methods=['GET'])
def get_stars_count():
  model = db.get_model()
  username = request.args.get('username')
  stars_count = model.count(username)
  return stars_count
