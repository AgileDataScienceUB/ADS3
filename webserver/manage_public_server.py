from flask_script import Manager
from public.app import app

manager = Manager(app)
app.config['DEBUG'] = True # Ensure debugger will load.

if __name__ == '__main__':
    manager.run()
