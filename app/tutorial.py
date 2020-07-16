from flask import Blueprint, render_template

bp = Blueprint('tutorial', __name__, url_prefix='/tutorial')

@bp.route('/index', methods=['GET'])
def index():
  return render_template('tutorial/index.html')