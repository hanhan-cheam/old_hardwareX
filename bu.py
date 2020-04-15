from flask import Flask
from flask_socketio import SocketIO
import eventlet
# Import Blueprints
from blueprints.endpoint1 import endpoint1_blueprint

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
eventlet.monkey_patch()
socketio = SocketIO(app, async_mode='eventlet')

@app.route('/')
def main():
    return "Hello, World"
 
# Blueprints registrations
app.register_blueprint(endpoint1_blueprint)

if __name__ == "__main__":
    socketio.run(app)