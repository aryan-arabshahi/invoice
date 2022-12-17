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
        """Find the specified contact by unique ID.

        Arguments:
            unique_id (str) -- The contact unique ID.

        Returns:
            Contact

        Raises:
            ContactNotFound
        """
        pass

    @abstractmethod
    def find(self, contact_id: str) -> Contact:
        """Find the specified contact by ID.

        Arguments:
            contact_id (str) -- The contact ID.

        Returns:
            Contact

        Raises:
            ContactNotFound
        """
        pass

    @abstractmethod
    def update(self, contact: Contact) -> Contact:
        """Update the specified contact

        Arguments:
            contact (Contact) -- The contact.

        Returns:
            Contact
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
        """Find the specified contact by unique ID.

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

    def find(self, contact_id: str) -> Contact:
        """Find the specified contact by ID.

        Arguments:
            contact_id (str) -- The contact ID.

        Returns:
            Contact

        Raises:
            ContactNotFound
        """
        self.logger.debug(f'Finding the contact by ID - id: {contact_id}')

        result = self.get_collection().find_one({'_id': self.str_to_object_id(contact_id)})

        if not result:
            raise ContactNotFound

        return Contact(**result)

    def update(self, contact: Contact) -> Contact:
        """Update the specified contact

        Arguments:
            contact (Contact) -- The contact.

        Returns:
            Contact
        """
        self.logger.debug(f'Updating the contact - contact: {contact}')

        contact.updatedAt = str(utcnow())

        self.get_collection().update_one(
            {
                '_id': self.str_to_object_id(contact.id),
            },
            {
                '$set': contact.get_changes(),
            }
        )

        return contact
