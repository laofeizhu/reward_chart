from config import Config
from flask import Flask
from flask_bootstrap import Bootstrap
import logging, coloredlogs

app = Flask(__name__)
logging.basicConfig(level=logging.WARNING)
coloredlogs.install()

app.config.from_object(Config)
Bootstrap(app)

from app import routes, db
import json

with app.app_context():
  model = db.get_model()
  model.init_app(app)

