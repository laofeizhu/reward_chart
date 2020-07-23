import functools

from app import db, models, app

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/register', methods=('GET', 'POST'))
def register():
  if request.method == 'POST':
    username = request.form['username']
    password = request.form['password']
    email = request.form['email']
    model = db.get_model()
    error = None

    if not username:
      error = 'Username is required.'
    elif not password:
      error = 'Password is required.'
    elif model.get_user(username_or_email=username) is not None:
      error = 'Username {} is already registered.'.format(username)
    elif model.get_user(username_or_email=email) is not None:
      error = 'Email {} is already registered.'.format(email)

    if error is None:
      user = models.User(username=username, email=email, password=generate_password_hash(password))
      model.register_user(user)
      session.clear()
      session['username'] = user.username
      return redirect(url_for('family.index'))

    flash(error)

  return render_template('auth/register.html')

@bp.route('/login', methods=('GET', 'POST'))
def login():
  error = None
  if request.method == 'POST':
    username_or_email = request.form['username_or_email']
    password = request.form['password']
    model = db.get_model()
    user = model.get_user(username_or_email=username_or_email)

    if user is None:
      error = 'Incorrect username.'
    elif not check_password_hash(user.password, password):
      error = 'Incorrect password.'

    if error is None:
      session.clear()
      session['username'] = user.username
      return redirect(url_for('family.console'))

    flash(error)

  return render_template('auth/login.html', error=error)

@bp.before_app_request
def load_logged_in_user():
    username = session.get('username')
    if username is None:
        g.user = None
    else:
        g.user = db.get_model().get_user(username_or_email=username)

@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view