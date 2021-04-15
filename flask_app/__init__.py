from flask import Flask
import os

app = Flask(__name__)

app.config['SECRET_KEY'] = 'secret-key'

from flask_app.ml_codes.views import ml_codes
app.register_blueprint(ml_codes)
