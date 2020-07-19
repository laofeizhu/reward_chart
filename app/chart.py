from app import db, app
from flask import Blueprint, render_template, g, request

bp = Blueprint('chart', __name__, url_prefix='/chart')

@bp.route('/index', methods=['GET'])
def index():
  model = db.get_model()
  child_id = request.args.get('child_id')
  if child_id is None:
    child_id = g.user.children[0]
  child = model.get_child(child_id)
  return render_template('chart/index.html', child=child)
