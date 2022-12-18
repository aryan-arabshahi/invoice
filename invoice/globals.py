from flask import Flask
from flask_cors import CORS
from invoice.services.contact import ContactService
from invoice.services.invoice import InvoiceService


flask_app = Flask(__name__)
CORS(flask_app)


# Services
contact_service = ContactService()
invoice_service = InvoiceService()
