from arrow import utcnow
from invoice.enums import CurrencyCodeEnum
from invoice.exceptions import InvoiceAlreadyExists
from invoice.globals import invoice_service, contact_service
from tests import BaseTest
from uuid import uuid4


class TestInvoice(BaseTest):

    def setUp(self):
        self.contact = contact_service.create(
            unique_id=self.generate_id(),
            name=self.faker.name(),
            organization=self.faker.name(),
            iban=str(uuid4())
        )

    def test_create_invoice_success(self):
        """The invoice creation success test
        """
        invoice = invoice_service.create(
            invoice_date=str(utcnow()),
            unique_id=self.generate_id(),
            amount_currency=CurrencyCodeEnum.EUR,
            amount_value=20,
            contact_id=self.contact.id
        )

        assert invoice.id

    def test_create_invoice_fail_already_exists(self):
        """The invoice creation fail already exists test
        """
        invoice = invoice_service.create(
            invoice_date=str(utcnow()),
            unique_id=self.generate_id(),
            amount_currency=CurrencyCodeEnum.EUR,
            amount_value=20,
            contact_id=self.contact.id
        )

        try:
            invoice_service.create(
                invoice_date=str(utcnow()),
                unique_id=invoice.uniqueId,
                amount_currency=CurrencyCodeEnum.EUR,
                amount_value=25.3,
                contact_id=self.contact.id
            )

        except InvoiceAlreadyExists as e:
            pass
