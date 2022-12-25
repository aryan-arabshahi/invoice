from flask import Response, request
from invoice.controllers import BaseController
from invoice.exceptions import ContactNotFound, InvoiceAlreadyExists
from invoice.globals import contact_service, invoice_service
from invoice.response import HttpResponse, HttpStatusCode


class InvoiceController(BaseController):

    def post(self) -> Response:
        """Add new invoice

        Returns:
            Response
        """
        response = HttpResponse()
        request_data = {}

        try:
            request_data = request.get_json(force=True)
            self.logger.debug(f'Creating the new invoice - {request_data}')

            contact_request_data = request_data.get('contact', {})

            self.logger.debug(f"Finding the contact - contact_unique_id: {contact_request_data.get('_id')}")

            contact = contact_service.create_or_update(
                unique_id=contact_request_data.get('_id'),
                name=contact_request_data.get('name'),
                organization=contact_request_data.get('organization'),
                iban=contact_request_data.get('iban')
            )

            invoice = invoice_service.create(
                invoice_date=request_data.get('invoiceDate'),
                unique_id=request_data.get('_id'),
                amount_currency=request_data.get('amount', {}).get('currencyCode'),
                amount_value=request_data.get('amount', {}).get('value'),
                contact_id=contact.id
            )

            return response.success(invoice.to_json(), http_status=HttpStatusCode.CREATED)

        except InvoiceAlreadyExists as e:
            self.log_errors(f'Could not create the new invoice - data: {request_data} - {e}')
            return response.fail(http_status=HttpStatusCode.CONFLICT, message='invoice_already_exists')

        except Exception as e:
            self.log_errors(f'Could not create the new contact - data: {request_data} - {e}')
            return response.fail(http_status=HttpStatusCode.INTERNAL_SERVER_ERROR, message='internal_server_error')
