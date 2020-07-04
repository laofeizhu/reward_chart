from config import Config
from flask import Flask
from flask_bootstrap import Bootstrap
from flask_migrate import Migrate
from flask_socketio import SocketIO
from flask_sqlalchemy import SQLAlchemy
import logging, coloredlogs

app = Flask(__name__)
logging.basicConfig(level=logging.WARNING)
coloredlogs.install()

app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
socketio = SocketIO(app)
Bootstrap(app)

from app import routes, models, socketio
import json

if __name__ == '__main__':
  socketio.run(app, debug=True)
