from flask_socketio import SocketIO, Namespace

class MyNamespace(Namespace):
    def on_connect(self):
        print('Client connected')
        self.emit('connected', {'data': 'You are connected'}) 

    def on_disconnect(self):
        print('Client disconnected')

    def on_my_event(self, data):
        print('Received data:', data)
        self.emit('response', {'message': 'Data received successfully'})

class SocketEvents:
    def __init__(self, socketio: SocketIO):
        self.socketio = socketio
        self.register_namespaces()

    def register_namespaces(self):
        self.socketio.on_namespace(MyNamespace('/mynamespace'))
