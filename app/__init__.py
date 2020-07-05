from config import Config
from flask import Flask
from flask_bootstrap import Bootstrap
from flask_socketio import SocketIO
import logging, coloredlogs

app = Flask(__name__)
logging.basicConfig(level=logging.WARNING)
coloredlogs.install()

app.config.from_object(Config)
socketio = SocketIO(app)
Bootstrap(app)

from app import routes, socketio, db
import json

with app.app_context():
  model = db.get_model()
  model.init_app(app)


if __name__ == '__main__':
  socketio.run(app, debug=True)
