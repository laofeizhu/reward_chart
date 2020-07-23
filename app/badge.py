import functools
import uuid

from app import db, models, app

from flask import (
    Blueprint, jsonify, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.utils import secure_filename

bp = Blueprint('badge', __name__, url_prefix='/badge')

@bp.route('/index', methods=('GET', 'POST'))
def index():
  if session.get('username') is None:
    return redirect(url_for('auth.login'))
  badges = []
  model = db.get_model()
  for badge_id in g.user.badges:
    badges.append(model.get_badge(badge_id))
  return render_template('badge/index.html', badges=badges)

@bp.route('/new_badge', methods=['GET', 'POST'])
def new_badge():
  if request.method == 'POST':
    name = request.form['name']
    model = db.get_model()
    error = None

    # TODO: verify that name is duplicated in user's badge list.
    if not name:
      error = 'Name is required.'

    if error is None:
      badge = models.Badge(name=name)
      if 'badge_image' in request.files:
        badge_image = request.files['badge_image']
        filename = secure_filename(str(uuid.uuid1()))
        model.save_file(filename, badge_image)
        badge.image_url = 'file/{}'.format(filename)
      model.register_badge(badge)
      model.add_badge_to_user(g.user.id, badge.id)
      g.user = db.get_model().get_user(id=g.user.id)
      return redirect(url_for('badge.index'))

    flash(error)
  return render_template('badge/new_badge.html')

@bp.route('/_get_badges_for_child/<child_id>')
def _get_bages_for_child(child_id):
  model = db.get_model()
  parent_ids = model.get_child(child_id).parents
  badge_ids = {}
  badges = []
  for parent_id in parent_ids:
    parent = model.get_user(id=parent_id)
    tmp_badge_ids = parent.badges
    for badge_id in tmp_badge_ids:
      if badge_id not in badge_ids:
        badge_ids[badge_id] = True
  for badge_id in badge_ids:
    badge = model.get_badge(badge_id)
    badges.append(badge.__dict__)
  return jsonify(badges)

@bp.route('/_score', methods=['GET', 'POST'])
def _score():
  model = db.get_model()
  child_id = request.args.get('child_id')
  badge_id = request.args.get('badge_id')
  utc_sec = request.args.get('timestamp')
  score = models.Score(badge=badge_id, timestamp=utc_sec)
  model.add_score(score=score, child_id=child_id)
  return 'score added'

@bp.route('/_scores_later_than', methods=['GET'])
def _scores_later_than():
  model = db.get_model()
  child_id = request.args.get('child_id')
  utc_sec = request.args.get('timestamp')
  child = model.get_child(id=child_id)
  resp = []
  for score_id in child.scores:
    score = model.get_score(id=score_id)
    if score.timestamp > utc_sec:
      resp.append({
        "id": score.id,
        "timestamp": int(score.timestamp),
        "image_url": model.get_badge(score.badge).image_url
      })
  return jsonify(resp)

@bp.route('/_delete_score', methods=['POST'])
def _delete_score():
  model = db.get_model()
  child_id = request.args.get('child_id')
  score_id = request.args.get('score_id')
  app.logger.info('deleting score %s for child %s' % (score_id, child_id))
  model.delete_score(score_id=score_id, child_id=child_id)
  return 'score deleted'

@bp.route('/_get_badges', methods=['GET'])
def _get_badges():
  model = db.get_model()
  badge_ids = g.user.badges
  badges = []
  for badge_id in badge_ids:
    badge = model.get_badge(badge_id)
    badges.append(badge.__dict__)
  return jsonify(badges)

@bp.route('/_delete_badge', methods=['POST'])
def _delete_badge():
  model = db.get_model()
  badge_id = request.args.get('badge_id')
  model.delete_badge(badge_id=badge_id, user_id=g.user.id)
  return 'badge deleted'