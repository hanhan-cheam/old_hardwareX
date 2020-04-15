import sys
sys.dont_write_bytecode = True
from flask_socketio import SocketIO
from app import create_app, create_socket

app = create_app()
socketio = create_socket()

if __name__ == "__main__":
    socketio.run(app, host='localhost', port=7777)