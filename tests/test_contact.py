from invoice.exceptions import ContactAlreadyExists, ContactNotFound
from invoice.globals import contact_service
from tests import BaseTest
from uuid import uuid4


class TestContact(BaseTest):

    def test_create_contact_success(self):
        """The create contact test method
        """
        contact = contact_service.create(
            unique_id=self.generate_id(),
            name=self.faker.name(),
            organization=self.faker.name(),
            iban=str(uuid4())
        )

        assert contact.id is not None

    def test_create_contact_fail_existed_contact(self):
        """The create existed contact test method
        """
        contact = contact_service.create(
            unique_id=self.generate_id(),
            name=self.faker.name(),
            organization=self.faker.name(),
            iban=str(uuid4())
        )

        try:
            contact_service.create(
                unique_id=contact.uniqueId,
                name=self.faker.name(),
                organization=self.faker.name(),
                iban=str(uuid4())
            )

            assert False

        except ContactAlreadyExists as e:
            pass

    def test_find_contact_by_unique_id_success(self):
        """Find contact by unique id success
        """
        contact = contact_service.create(
            unique_id=self.generate_id(),
            name=self.faker.name(),
            organization=self.faker.name(),
            iban=str(uuid4())
        )

        result = contact_service.find_by_unique_id(contact.uniqueId)

        assert result.id == contact.id

    def test_find_contact_by_unique_id_fail_not_found(self):
        """Find contact by unique id success
        """
        try:
            contact_service.find_by_unique_id(self.generate_id())

        except ContactNotFound as e:
            pass

    def test_find_contact_by_id_success(self):
        """The find contact by ID success test
        """
        contact = contact_service.create(
            unique_id=self.generate_id(),
            name=self.faker.name(),
            organization=self.faker.name(),
            iban=str(uuid4())
        )

        result = contact_service.find(contact.id)

        assert result.id == contact.id

    def test_find_contact_by_id_fail_not_found(self):
        """The find contact by ID fail not found test
        """
        try:
            contact_service.find(self.generate_id())

        except ContactNotFound as e:
            pass

    def test_update_contact_success(self):
        """The find contact by ID success test
        """
        contact = contact_service.create(
            unique_id=self.generate_id(),
            name=self.faker.name(),
            organization=self.faker.name(),
            iban=str(uuid4())
        )

        updated_contact = contact_service.update(
            contact.id,
            {
                'name': self.faker.name(),
                'organization': self.faker.name(),
                'iban': str(uuid4()),
            }
        )

        assert contact.iban != updated_contact.iban and contact.updatedAt != updated_contact.updatedAt

    def test_update_contact_fail_not_found(self):
        """The update contact success not found test
        """
        try:
            contact_service.update(
                self.generate_id(),
                {
                    'name': self.faker.name(),
                    'organization': self.faker.name(),
                    'iban': str(uuid4()),
                }
            )

        except ContactNotFound as e:
            pass
