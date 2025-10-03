# webserver.py
from flask import Flask, request
from flask_cors import CORS
from flask_socketio import SocketIO, emit
from WebserverApp.apiOffices.oh import apiOh


app = Flask(__name__)
CORS(app)
app.config['SECRET_KEY'] = 'your_secret_key'
socketio = SocketIO(app, cors_allowed_origins="*")

app.register_blueprint(apiOh, url_prefix='/api')

@app.route('/') 
def index():
    return 'Botsito de CS50 o WEB JAJJAJAJ'


@socketio.on('connect')
def handle_connect():
    print('Client connected')
    socketio.emit('connected', {'data': 'pipi'})

    
@socketio.on('message')
def handle_message(data):
    print(f'Received message: {data}')
    emit('response', {'data': f'Server received: {data}'}, broadcast=True) # Broadcast to all connected clients
    
@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected')


# event handler for customer ordering food
@socketio.on("order_food")
def handle_event(data):

    emit("send_food", {'data':'pipi'}, broadcast=True)