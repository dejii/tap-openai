"""REST client handling, including OpenAIStream base class."""

from __future__ import annotations

import decimal
import typing as t

from singer_sdk.authenticators import BearerTokenAuthenticator
from singer_sdk.helpers.jsonpath import extract_jsonpath
from singer_sdk.pagination import BaseAPIPaginator  # noqa: TCH002
from singer_sdk.streams import RESTStream
from datetime import datetime

if t.TYPE_CHECKING:
    import requests
    from singer_sdk.helpers.types import Context


class OpenAIStream(RESTStream):
    """OpenAi stream class."""

    records_jsonpath = "$[*]"

    next_page_token_jsonpath = "$.next_page"  # noqa: S105

    @property
    def url_base(self) -> str:
        return "https://api.openai.com"

    @property
    def authenticator(self) -> BearerTokenAuthenticator:
        """Return a new authenticator object.

        Returns:
            An authenticator instance.
        """
        return BearerTokenAuthenticator.create_for_stream(
            self,
            token=self.config.get("auth_token", ""),
        )

    @property
    def http_headers(self) -> dict:
        """Return the http headers needed.

        Returns:
            A dictionary of HTTP headers.
        """
        # If not using an authenticator, you may also provide inline auth headers:
        # headers["Private-Token"] = self.config.get("auth_token")  # noqa: ERA001
        return {}

    def get_new_paginator(self) -> BaseAPIPaginator:
        """Create a new pagination helper instance.

        If the source API can make use of the `next_page_token_jsonpath`
        attribute, or it contains a `X-Next-Page` header in the response
        then you can remove this method.

        If you need custom pagination that uses page numbers, "next" links, or
        other approaches, please read the guide: https://sdk.meltano.com/en/v0.25.0/guides/pagination-classes.html.

        Returns:
            A pagination helper instance.
        """
        return super().get_new_paginator()

    def get_url_params(
        self,
        context: Context | None,  # noqa: ARG002
        next_page_token: t.Any | None,  # noqa: ANN401
    ) -> dict[str, t.Any]:
        """Return a dictionary of values to be used in URL parameterization.

        Args:
            context: The stream context.
            next_page_token: The next page index or value.

        Returns:
            A dictionary of URL query parameters.
        """
        params: dict = {}
        start_date = datetime.strptime(
            self.config.get("start_date"), "%Y-%m-%dT%H:%M:%SZ"
        )
        end_date = datetime.strptime(self.config.get("end_date"), "%Y-%m-%dT%H:%M:%SZ")
        params["start_date"] = start_date.date()
        params["end_date"] = end_date.date()
        params["exclude_project_costs"] = self.config.get("exclude_project_costs")
        params["file_format"] = self.config.get("file_format")
        params["group_by"] = self.config.get("group_by")
        params["new_endpoint"] = self.config.get("new_endpoint")
        return params

    # def validate_response(self, response: requests.Response) -> None:
    #     logging.warning(response.json())

    def parse_response(self, response: requests.Response) -> t.Iterable[dict]:
        """Parse the response and return an iterator of result records.

        Args:
            response: The HTTP ``requests.Response`` object.

        Yields:
            Each record from the source.
        """
        yield from extract_jsonpath(
            self.records_jsonpath,
            input=response.json(parse_float=decimal.Decimal),
        )
