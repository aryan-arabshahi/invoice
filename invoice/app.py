from flask_restful import Api
from . import config
from .controllers.contact import ContactListController, ContactByOrganizationAndNameController
from .controllers.invoice import InvoiceController
from .globals import flask_app


class InvoiceApp:

    def __init__(self):
        self._flask_api = Api(flask_app, prefix='/api')
        self.setup()

    def setup(self) -> None:
        """Set up the API resources
        """
        self._flask_api.add_resource(ContactListController, '/contacts')
        self._flask_api.add_resource(ContactByOrganizationAndNameController, '/contacts/<string:organization>/<string:name>')
        self._flask_api.add_resource(InvoiceController, '/invoices')

    @staticmethod
    def run() -> None:
        """Run the application
        """
        flask_app.run(host=config.get('host', '0.0.0.0'), debug=config.get('debug', False))
