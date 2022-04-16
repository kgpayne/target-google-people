"""GooglePeople target class."""

from singer_sdk.target_base import Target
from singer_sdk import typing as th

from target_google_people.sinks import (
    GooglePeopleSink,
)


class TargetGooglePeople(Target):
    """Sample target for GooglePeople."""

    name = "target-google-people"
    config_jsonschema = th.PropertiesList(
        th.Property(
            "client_secret_path",
            th.StringType,
            description="The path to the Google client_secret.json file."
        ),
        th.Property(
            "token_path",
            th.StringType,
            description="The path to store the generated token.json auth file."
        ),
    ).to_dict()
    default_sink_class = GooglePeopleSink
