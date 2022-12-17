from flask import Response, request
from invoice.controllers import BaseController
from invoice.exceptions import ContactAlreadyExists
from invoice.globals import contact_service
from invoice.response import HttpResponse, HttpStatusCode


class ContactController(BaseController):

    def post(self) -> Response:
        """Add new user

        Returns:
            Response
        """
        response = HttpResponse()
        request_data = {}

        try:
            request_data = request.get_json(force=True)
            self.logger.debug(f'Creating the new contact - {request_data}')

            contact = contact_service.create(
                unique_id=request_data.get('_id'),
                name=request_data.get('name'),
                organization=request_data.get('organization'),
                iban=request_data.get('iban')
            )

            return response.success(contact.to_json(), http_status=HttpStatusCode.CREATED)

        except ContactAlreadyExists as e:
            self.log_errors(f"The contact already exists. - unique_id: {request_data.get('unique_id')} - {e}")
            return response.fail(http_status=HttpStatusCode.CONFLICT, message='contact_already_exists')

        except Exception as e:
            self.log_errors(f'Could not create the new contact - data: {request_data} - {e}')
            return response.fail(http_status=HttpStatusCode.INTERNAL_SERVER_ERROR, message='internal_server_error')
