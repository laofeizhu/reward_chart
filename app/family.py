import functools
import uuid

from app import db, models, app

from flask import (
    Blueprint, jsonify, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.utils import secure_filename

bp = Blueprint('family', __name__, url_prefix='/family')

@bp.route('/index', methods=['GET', 'POST'])
def index():
  if session.get('username') is None:
    return redirect(url_for('auth.login'))
  children = []
  model = db.get_model()
  for child_id in g.user.children:
    children.append(model.get_child(child_id))
  return render_template('family/index.html', children=children)

@bp.route('/new_child', methods=['GET', 'POST'])
def new_child():
  if request.method == 'POST':
    name = request.form['name']
    model = db.get_model()
    error = None

    # TODO: verify that name is duplicated in user's children list.
    if not name:
      error = 'Name is required.'

    if error is None:
      child = models.Child(name=name)
      if 'profile_image' in request.files:
        profile_image = request.files['profile_image']
        filename = secure_filename(str(uuid.uuid1()))
        model.save_file(filename, profile_image)
        child.avatar_url = filename
      child.parents.append(g.user.id)
      model.register_child(child)
      model.add_child(g.user.id, child.id)
      g.user = db.get_model().get_user(id=g.user.id)
      return redirect(url_for('family.index'))

    flash(error)
  return render_template('family/new_child.html')

@bp.route('/_child_score_count', methods=['GET'])
def _child_score_count():
  model = db.get_model()
  child_id = request.args.get('child_id')
  child_score_count = model.get_child_score_count(child_id)
  return jsonify(child_score_count)

@bp.route('/_child_score_balance', methods=['GET'])
def _child_score_balance():
  model = db.get_model()
  child_id = request.args.get('child_id')
  child = model.get_child(child_id)
  return jsonify(child.score_balance)

@bp.route('/_get_children', methods=['GET'])
def _get_children():
  model = db.get_model()
  children = []
  for child_id in g.user.children:
    child = model.get_child(child_id)
    children.append(child.__dict__)
  return jsonify(children)

@bp.route('/_delete_child', methods=['POST'])
def _delete_child():
  model = db.get_model()
  child_id = request.args.get('child_id')
  model.delete_child(child_id=child_id, user_id=g.user.id)
  return 'child removed from user'

DEFAULT_REWARD = models.Reward(id='default-reward-ns', image_url='static/images/nintendoswitch.jpg', name='Nintendo Switch', score=50)
@bp.route('/_current_reward', methods=['GET'])
def _current_reward():
  model = db.get_model()
  child_id = request.args.get('child_id')
  reward = model.get_current_reward(child_id)
  if reward is None:
    reward = DEFAULT_REWARD
  return jsonify(reward.__dict__)