from arrow import utcnow
from invoice.dataclasses import Contact
from invoice.exceptions import ContactNotFound
from invoice.repositories import BaseRepository
from abc import ABC, abstractmethod


class ContactRepositoryInterface(ABC):

    @abstractmethod
    def create(self, contact: Contact) -> Contact:
        """Create the specified contact.

        Arguments:
            contact (Contact)

        Returns:
            Contact
        """
        pass

    @abstractmethod
    def find_by_unique_id(self, unique_id: str) -> Contact:
        """Find the specified contact.

        Arguments:
            unique_id (str) -- The contact unique ID.

        Returns:
            Contact

        Raises:
            ContactNotFound
        """
        pass


class ContactRepository(BaseRepository, ContactRepositoryInterface):

    COLLECTION = 'contacts'

    def create(self, contact: Contact) -> Contact:
        """Create the specified contact.

        Arguments:
            contact (Contact)

        Returns:
            Contact
        """
        self.logger.debug(f'Creating the contact - {contact}')
        now = utcnow()
        contact.createdAt = now
        contact.updatedAt = None
        result = self.get_collection().insert_one(contact.to_json(insert_mode=True))
        contact.id = str(result.inserted_id)
        self.logger.debug(f'The contact has been created - {contact}')
        return contact

    def find_by_unique_id(self, unique_id: str) -> Contact:
        """Find the specified contact.

        Arguments:
            unique_id (str) -- The contact unique ID.

        Returns:
            Contact

        Raises:
            ContactNotFound
        """
        self.logger.debug(f'Finding the contact by unique ID - unique_id: {unique_id}')

        result = self.get_collection().find_one({'uniqueId': unique_id})

        if not result:
            raise ContactNotFound

        return Contact(**result)
