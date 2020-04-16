from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_socketio import SocketIO
from flask_cors import CORS
import eventlet

db = SQLAlchemy()
socketio = SocketIO()
migrate = Migrate()

def create_app():
    app = Flask(__name__, instance_relative_config=False)
    CORS(app)
    app.config.from_object('config.Config')
    eventlet.monkey_patch()
    socketio.init_app(app, cors_allowed_origins='*', async_mode='eventlet')
    db.init_app(app)
    migrate.init_app(app, db)

    with app.app_context():
        from . import routes
        from . import wsroutes
        from .models import user, address
        from .blueprints import user

        app.register_blueprint(user.user_blueprint)
        db.create_all()

        return app
