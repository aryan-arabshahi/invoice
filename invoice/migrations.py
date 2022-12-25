from invoice.repositories.contact import ContactRepository


class Migrate:

    @staticmethod
    def run() -> None:
        """Run eth migrations
        """
        contact_repository = ContactRepository()
        try:
            contact_repository.get_collection().create_index(
                [('name', 'text')],
                name='contacts_name_text_index',
                background=True
            )

        except Exception as e:
            raise Exception(f'Could not run the migrations. - {e}')
