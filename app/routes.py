from flask import current_app as app
from flask import render_template
from . import create_socket

socketio = create_socket()

@app.route('/')
def home():
    # Landing page.
    return "Hello, World"

@socketio.on('message')
def handle_message(message):
    print('received message:' + message)