from invoice.repositories.contact import ContactRepository
from invoice.services import BaseService


class ContactService(BaseService):

    def __init__(self):
        super().__init__()
        self._contact_repository = ContactRepository()
