from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_socketio import SocketIO
import eventlet
db = SQLAlchemy()

def create_app():
    app = Flask(__name__, instance_relative_config=False)
    CORS(app)
    app.config.from_object('config.Config')
    db.init_app(app)
    Migrate(app, db)

    with app.app_context():
        from . import routes
        from .models import user, address
        from .blueprints import user

        app.register_blueprint(user.user_blueprint)
        db.create_all()

        return app

def create_socket():
    socketio = SocketIO(create_app(), async_mode='eventlet')
    eventlet.monkey_patch()
    return socketio
