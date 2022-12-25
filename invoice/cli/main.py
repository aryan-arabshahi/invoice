from invoice.app import InvoiceApp
from invoice.logger import Logger
from invoice.migrations import Migrate


def main():
    Logger.setup()
    app = InvoiceApp()
    app.run()


def migrate():
    Migrate.run()


if __name__ == '__main__':
    main()
