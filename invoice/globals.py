from flask import Flask
from flask_cors import CORS
from invoice.services.contact import ContactService


flask_app = Flask(__name__)
CORS(flask_app)


# Services
contact_service = ContactService()
