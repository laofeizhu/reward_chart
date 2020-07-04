from app import app
from app import socketio
import json

def msgReceived(methods=['GET', 'POST']):
  app.logger.info('message was received')

def update_star():
  app.logger.info('sending star count')
  resp = {'star_count': 1}
  socketio.emit('update star', json.dumps(resp), callback=msgReceived)

@socketio.on('my event')
def handle_event(payload, methods=['GET', 'POST']):
  app.logger.info('received event: ' + str(payload))
  update_star()

@socketio.on('add star')
def handle_add_star(json, methods=['GET', 'POST']):
  app.logger.info('adding star')
  update_star()
