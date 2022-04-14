"""GooglePeople target sink class, which handles writing streams."""


from singer_sdk.sinks import RecordSink

from target_google_people.google_people_service import GooglePeopleService


class GooglePeopleSink(RecordSink):
    """GooglePeople target sink class."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.gps = GooglePeopleService()

    def process_record(self, record: dict, context: dict) -> None:
        """Process the record."""
        body = {
            "first_name": record["first_name"],
            "last_name": record["last_name"],
            "email_address": record["email_address"],
            "contact_group_name": record.get("contact_group_name")
        }
        self.gps.create_contact(**body)
