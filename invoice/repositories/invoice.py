from arrow import utcnow

from invoice.dataclasses import Invoice
from invoice.exceptions import InvoiceNotFound
from invoice.repositories import BaseRepository
from abc import ABC, abstractmethod


class InvoiceRepositoryInterface(ABC):

    @abstractmethod
    def create(self, invoice: Invoice) -> Invoice:
        """Create the specified invoice.

        Arguments:
            invoice (Invoice)

        Returns:
            Invoice
        """
        pass

    @abstractmethod
    def find_by_unique_id(self, unique_id: str) -> Invoice:
        """Find the specified invoice by unique ID.

        Arguments:
            unique_id (str) -- The invoice unique ID.

        Returns:
            invoice

        Raises:
            InvoiceNotFound
        """
        pass


class InvoiceRepository(BaseRepository, InvoiceRepositoryInterface):

    COLLECTION = 'invoices'

    def create(self, invoice: Invoice) -> Invoice:
        """Create the specified invoice.

        Arguments:
            invoice (Invoice)

        Returns:
            Invoice
        """
        self.logger.debug(f'Creating the invoice - {invoice}')
        now = utcnow()
        invoice.createdAt = now
        invoice.updatedAt = None
        result = self.get_collection().insert_one(invoice.to_json(insert_mode=True))
        invoice.id = str(result.inserted_id)
        self.logger.debug(f'The invoice has been created - {invoice}')
        return invoice

    def find_by_unique_id(self, unique_id: str) -> Invoice:
        """Find the specified invoice by unique ID.

        Arguments:
            unique_id (str) -- The invoice unique ID.

        Returns:
            invoice

        Raises:
            InvoiceNotFound
        """
        self.logger.debug(f'Finding the invoice by unique ID - unique_id: {unique_id}')

        result = self.get_collection().find_one({'uniqueId': unique_id})

        if not result:
            raise InvoiceNotFound

        return Invoice(**result)
