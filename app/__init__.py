from flask import Flask

app = Flask(__name__)
app.config.from_object('config')
app.config.from_object('instance.config')

from app import views
