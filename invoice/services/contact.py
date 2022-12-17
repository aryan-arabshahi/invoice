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
            self.find_by_unique_id(unique_id)

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

    def find_by_unique_id(self, unique_id: str) -> Contact:
        """Find the specified contact by unique ID

        Arguments:
            unique_id (str) -- The contact unique ID.

        Returns:
            Contact

        Raises:
            ContactNotFound -- The contact not found exception.
        """
        self.logger.debug(f'Finding the specified contact by unique ID - unique_id: {unique_id}')

        return self._contact_repository.find_by_unique_id(unique_id)

    def update(self, contact_id: str, data: dict) -> Contact:
        """Update the specified contact

        Arguments:
            contact_id (str) -- The contact ID.
            data (dict) -- The update data.

        Returns:
            Contact

        Raises:
            ContactNotFound -- The contact not found exception.
        """
        self.logger.debug(f'Updating the specified contact by ID - id: {contact_id}')

        contact = self.find(contact_id)

        contact.update(data)

        return self._contact_repository.update(contact)

    def find(self, contact_id: str) -> Contact:
        """Find specified contact.

        Arguments:
            contact_id (str) -- The contact ID.

        Returns:
            Contact

        Raises:
            ContactNotFound -- The contact not found exception.
        """
        self.logger.debug(f'Finding the specified contact by ID - id: {contact_id}')

        return self._contact_repository.find(contact_id)
