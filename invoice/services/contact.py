from invoice.dataclasses import Contact
from invoice.exceptions import ContactAlreadyExists, ContactNotFound
from invoice.repositories.contact import ContactRepository
from invoice.services import BaseService


class ContactService(BaseService):

    def __init__(self):
        super().__init__()
        self._contact_repository = ContactRepository()

    def create(self, unique_id: str, name: str, organization: str, iban: str) -> Contact:
        """Create the specified contact

        Arguments:
            unique_id (str) -- The unique ID
            name (str) -- The name
            organization (str) -- The organization
            iban (str) -- The IBAN

        Returns:
            Contact

        Raises:
            ContactAlreadyExists -- The contact already exists.
        """
        self.logger.debug(f'Creating the specified contact - unique_id: {unique_id} - name: {name} - '
                          f'organization: {organization}')

        try:
            self._contact_repository.find_by_unique_id(unique_id)

            raise ContactAlreadyExists

        except ContactNotFound as e:
            pass

        contact = Contact(
            uniqueId=unique_id,
            name=name,
            organization=organization,
            iban=iban
        )

        return self._contact_repository.create(contact)
