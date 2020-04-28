import os, sys
sys.dont_write_bytecode = True
from app import create_app, socketio
from dotenv import load_dotenv
load_dotenv()
import threading
from app import server


app = create_app()

if __name__ == "__main__":
    socketio.run(app, host='127.0.0.1', port=os.getenv('FLASK_RUN_PORT'))
