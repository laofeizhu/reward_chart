import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
  MONGO_URI = 'mongodb+srv://kevin-li:almighty78@cluster0-m05c3.gcp.mongodb.net/rc2_test?retryWrites=true&w=majority'

  SECRET_KEY = 'ethan_s_reward_chart'
