from flask import Flask
import os

app = Flask(__name__)
app.config.from_object('config')
if 'instance' in os.listdir() and 'config.py' in os.listdir('instance'):
    app.config.from_object('instance.config')
if os.environ.get('MLAB_USER'):
    app.config['MLAB_USER'] = os.environ.get('MLAB_USER')
if os.environ.get('MLAB_PASSWORD'):
    app.config['MLAB_PASSWORD'] = os.environ.get('MLAB_PASSWORD')