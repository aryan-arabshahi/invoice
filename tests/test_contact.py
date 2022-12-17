from invoice.exceptions import ContactAlreadyExists
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
