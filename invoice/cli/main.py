from invoice.app import InvoiceApp
from invoice.logger import Logger


def main():
    Logger.setup()
    app = InvoiceApp()
    app.run()


if __name__ == '__main__':
    main()
