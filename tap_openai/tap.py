"""OpenAi tap class."""

from __future__ import annotations

from singer_sdk import Tap
from singer_sdk import typing as th

# TODO: Import your custom stream types here:
from tap_openai import streams


class TapOpenAI(Tap):
    """OpenAI tap class."""

    name = "tap-openai"

    config_jsonschema = th.PropertiesList(
        th.Property(
            "auth_token",
            th.StringType,
            required=True,
            secret=True,
            title="API Key",
            description="The token to authenticate against the API service",
        ),
        th.Property(
            "start_date",
            th.DateTimeType,
            required=True,
            title="Start Date",
            description="Start Date for the data to be fetched",
        ),
        th.Property(
            "end_date",
            th.DateTimeType,
            required=True,
            title="End Date",
            description="End Date for the data to be fetched",
        ),
        th.Property(
            "exclude_project_costs",
            th.BooleanType,
            required=True,
            description="Exclude project costs",
        ),
        th.Property(
            "file_format",
            th.StringType,
            required=True,
            description="The earliest record date to sync",
        ),
        th.Property(
            "group_by",
            th.StringType,
            required=True,
            description="Columns to group by",
        ),
        th.Property("new_endpoint", th.BooleanType, default=True),
    ).to_dict()

    def discover_streams(self) -> list[streams.OpenAIStream]:
        """Return a list of discovered streams.

        Returns:
            A list of discovered streams.
        """
        return [
            streams.BillingUsageStream(self),
        ]


if __name__ == "__main__":
    TapOpenAI.cli()
