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
            "filepath",
            th.StringType,
            description="The path to the target output file"
        ),
        th.Property(
            "file_naming_scheme",
            th.StringType,
            description="The scheme with which output files will be named"
        ),
    ).to_dict()
    default_sink_class = GooglePeopleSink
