from config import Config
from flask import Flask
from flask_bootstrap import Bootstrap
import logging, coloredlogs

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)
coloredlogs.install()

app.config.from_object(Config)
Bootstrap(app)

from app import routes, db, auth, family, reward, badge

app.register_blueprint(auth.bp)
app.register_blueprint(family.bp)
app.register_blueprint(reward.bp)
app.register_blueprint(badge.bp)

model = db.get_model()
model.init_app(app)

