from flask_restful import Api

from . import config
from .controllers.contact import ContactController
from .globals import flask_app


class InvoiceApp:

    def __init__(self):
        self._flask_api = Api(flask_app, prefix='/api')
        self.setup()

    def setup(self) -> None:
        """Set up the API resources
        """
        self._flask_api.add_resource(ContactController, '/contacts')

    @staticmethod
    def run() -> None:
        """Run the application
        """
        flask_app.run(debug=config.get('debug', False))
