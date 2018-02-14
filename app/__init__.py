from flask import Flask
import os

app = Flask(__name__)
app.config.from_object('config')
if 'instance' in os.listdir() and 'config.py' in os.listdir('instance'):
    app.config.from_object('instance.config')
