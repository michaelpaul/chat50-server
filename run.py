#!/usr/bin/env python
from chat50 import create_app
from chat50.websocket import socketio

app = create_app()

if __name__ == '__main__':    
    socketio.run(app)
