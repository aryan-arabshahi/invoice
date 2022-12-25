from invoice.app import InvoiceApp
from invoice.logger import Logger
from sys import argv
from invoice.migrations import Migrate


def main():
    Logger.setup()
    app = InvoiceApp()
    app.run()


def migrate():
    Migrate.run()


if __name__ == '__main__':
    args = argv[1:]
    if args and args[0] == '--migrate':
        migrate()
    else:
        main()
