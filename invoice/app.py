from .globals import config


class InvoiceApp:

    @staticmethod
    def run() -> None:
        """Run the application
        """
        host = config.get('mongodb.host')
