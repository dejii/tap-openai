"""Stream type classes for tap-openai."""

from __future__ import annotations

import typing as t

from singer_sdk import typing as th

from tap_openai.client import OpenAiStream


class BillingUsageStream(OpenAiStream):
    """Define custom stream."""

    name = "billing_usage"
    path = "/v1/dashboard//billing/usage/export"
    primary_keys: t.ClassVar[list[str]] = ["user_id", "name", "date"]
    replication_key = "timestamp"
    schema = th.PropertiesList(
        th.Property("currency", th.StringType),
        th.Property("name", th.StringType),
        th.Property("cost", th.NumberType),
        th.Property("user_id", th.StringType),
        th.Property("user_email", th.StringType),
        th.Property("cost_in_major", th.StringType),
        th.Property("date", th.DateType),
        th.Property("timestamp", th.IntegerType),
    ).to_dict()
