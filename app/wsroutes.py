from . import socketio

@socketio.on('connect')
def test_connect():
    print('Client Connectedsss')

@socketio.on('disconnect')
def test_disconnect():
    print('Client disconnected')