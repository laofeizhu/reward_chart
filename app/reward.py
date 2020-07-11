import functools
import uuid

from app import db, models, app

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.utils import secure_filename

bp = Blueprint('reward', __name__, url_prefix='/reward')

@bp.route('/console', methods=('GET', 'POST'))
def console():
  if session.get('username') is None:
    return redirect(url_for('auth.login'))
  rewards = []
  model = db.get_model()
  for reward_id in g.user.rewards:
    rewards.append(model.get_reward(reward_id))
  app.logger.info('rewards are {}'.format(rewards))
  return render_template('reward/console.html', rewards=rewards)

@bp.route('/new_reward', methods=('GET', 'POST'))
def new_reward():
  if request.method == 'POST':
    name = request.form['name']
    model = db.get_model()
    error = None

    # TODO: verify that name is duplicated in user's rewardren list.
    if not name:
      error = 'Name is required.'

    if error is None:
      reward = models.Reward(name=name)
      if 'reward_image' in request.files:
        reward_image = request.files['reward_image']
        filename = secure_filename(str(uuid.uuid1()))
        model.save_file(filename, reward_image)
        reward.image_url = filename
      model.register_reward(reward)
      model.add_reward_to_user(g.user.id, reward.id)
      g.user = db.get_model().get_user(id=g.user.id)
      return redirect(url_for('reward.console'))

    flash(error)
  return render_template('reward/new_reward.html')
