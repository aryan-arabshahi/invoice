from flask import Response, request
from invoice.controllers import BaseController
from invoice.response import HttpResponse


class ContactController(BaseController):

    def post(self) -> Response:
        """Add new user

        Returns:
            Response
        """
        response = HttpResponse()
        request_data = request.get_json(force=True)
        self.logger.debug(f'Creating the new contact - {request_data}')
        try:
            created_user = contact_service.create(
                email=inputs.email,
                first_name=inputs.first_name,
                last_name=inputs.last_name,
                image=inputs.image,
                wage=inputs.wage
            )

            return response.success()

        except Exception as e:
            self.log_errors(f'Could not create the new contact - email: {request_data} - {e}')
            return response.failed(http_status=500, message='internal_server_error')
