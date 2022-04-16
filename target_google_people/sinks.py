"""GooglePeople target sink class, which handles writing streams."""


from singer_sdk.sinks import RecordSink

from target_google_people.google_people_service import GooglePeopleService


class GooglePeopleSink(RecordSink):
    """GooglePeople target sink class."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.gps = GooglePeopleService(
            client_secret_path=self.config.get("client_secret_path"),
            token_path=self.config.get("token_path")
        )

    def process_record(self, record: dict, context: dict) -> None:
        """Process the record."""
        if self.stream_name == 'contacts':
            body = {
                "first_name": record["first_name"],
                "last_name": record["last_name"],
                "email_address": record["email_address"],
                "contact_group_name": record.get("contact_group_name")
            }
            self.gps.upsert_contact(**body)
