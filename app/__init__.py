from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_socketio import SocketIO
from flask_cors import CORS
import eventlet
# eventlet.monkey_patch()
import threading

db = SQLAlchemy()
socketio = SocketIO()
migrate = Migrate()
app = Flask(__name__, instance_relative_config=False)
def create_app():
    # app = Flask(__name__, instance_relative_config=False)
    CORS(app)
    app.config.from_object('config.Config')
    eventlet.monkey_patch()
    socketio.init_app(app, cors_allowed_origins='*', async_mode='eventlet')
    db.init_app(app)
    migrate.init_app(app, db)

    with app.app_context():
        from . import routes
        # from . import wsroutes
        from .blueprints.station import wsroutes
        from .models import user, address, bin, fake_bin_weight, ip_port, station
        from .blueprints import user
        from .blueprints.station import routes,common
        from . import server
        from app.database import bin

        # bin.InsertUpdateBin("gaga","1","3")
        

        app.register_blueprint(routes.station_blueprint)
        app.register_blueprint(user.user_blueprint)
        db.create_all()
        eventlet.spawn(server.startServer)
        eventlet.spawn(common.broadcastLoop)
    
        return app
