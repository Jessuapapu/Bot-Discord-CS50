from flask import Flask
from threading import Thread

app = Flask('')


@app.route('/')
def index():
    return 'Botsito de CS50 JAJJAJAJ'

def run():
    app.run(host="0.0.0.0",port=8000)
    
def keep_alive():
    server = Thread(target=run)
    server.start()