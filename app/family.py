import functools
import uuid

from app import db, models, app

from flask import (
    Blueprint, jsonify, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.utils import secure_filename

bp = Blueprint('family', __name__, url_prefix='/family')

@bp.route('/console', methods=['GET', 'POST'])
def console():
  if session.get('username') is None:
    return redirect(url_for('auth.login'))
  children = []
  model = db.get_model()
  for child_id in g.user.children:
    children.append(model.get_child(child_id))
  return render_template('family/console.html', children=children)

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
      return redirect(url_for('family.console'))

    flash(error)
  return render_template('family/new_child.html')

@bp.route('/reward_chart/<id>', methods=['GET'])
def reward_chart(id):
  model = db.get_model()
  child = model.get_child(id)
  return render_template('family/reward_chart.html', child=child)

@bp.route('/_child_score_count', methods=['GET'])
def _child_score_count():
  model = db.get_model()
  child_id = request.args.get('child_id')
  child_score_count = model.get_child_score_count(child_id)
  return jsonify(child_score_count)