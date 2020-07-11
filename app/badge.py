import functools
import uuid

from app import db, models, app

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.utils import secure_filename

bp = Blueprint('badge', __name__, url_prefix='/badge')

@bp.route('/console', methods=('GET', 'POST'))
def console():
  if session.get('username') is None:
    return redirect(url_for('auth.login'))
  badges = []
  model = db.get_model()
  for badge_id in g.user.badges:
    badges.append(model.get_badge(badge_id))
  return render_template('badge/console.html', badges=badges)

@bp.route('/new_badge', methods=('GET', 'POST'))
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
        badge.image_url = filename
      model.register_badge(badge)
      model.add_badge_to_user(g.user.id, badge.id)
      g.user = db.get_model().get_user(id=g.user.id)
      return redirect(url_for('badge.console'))

    flash(error)
  return render_template('badge/new_badge.html')
