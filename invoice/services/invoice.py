from invoice.dataclasses import Invoice, InvoiceAmount
from invoice.enums import CurrencyCodeEnum
from invoice.exceptions import InvoiceNotFound, InvoiceAlreadyExists
from invoice.repositories.invoice import InvoiceRepository
from invoice.services import BaseService


class InvoiceService(BaseService):

    def __init__(self):
        super().__init__()
        self._invoice_repository = InvoiceRepository()

    def find_by_unique_id(self, unique_id: str) -> Invoice:
        """Find the specified invoice by unique ID

        Arguments:
            unique_id (str) -- The invoice unique ID.

        Returns:
            invoice

        Raises:
            InvoiceNotFound -- The invoice not found exception.
        """
        self.logger.debug(f'Finding the specified invoice by unique ID - unique_id: {unique_id}')

        return self._invoice_repository.find_by_unique_id(unique_id)

    def create(self, invoice_date: str, unique_id: str, amount_currency: str, amount_value: float,
               contact_id: str) -> Invoice:
        """Create the new invoice

        Arguments:
            invoice_date (str) -- The invoice date.
            unique_id (str) -- The unique ID.
            amount_currency (str) -- The amount currency.
            amount_value (float) -- The amount value.
            contact_id (str) -- The contact ID.

        Returns:
            Invoice

        Raises:
            InvoiceAlreadyExists -- The invoice already exists exception.
        """
        self.logger.debug(f'Creating the new invoice - unique_id: {unique_id} - contact_id: {contact_id}')

        invoice_amount = InvoiceAmount(currencyCode=CurrencyCodeEnum(amount_currency), value=amount_value)

        try:
            self.find_by_unique_id(unique_id)
            raise InvoiceAlreadyExists

        except InvoiceNotFound as e:
            pass

        invoice = Invoice(
            invoiceDate=invoice_date,
            uniqueId=unique_id,
            amount=invoice_amount,
            contactId=contact_id
        )

        return self._invoice_repository.create(invoice)
