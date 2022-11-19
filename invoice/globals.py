from flask import Flask
from flask_cors import CORS
from invoice.config import Config


config = Config()

flask_app = Flask(__name__)
CORS(flask_app)
