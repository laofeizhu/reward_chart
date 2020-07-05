from app import app, db

@app.shell_context_processor
def make_shell_context():
  return {'model': db.get_model()}
