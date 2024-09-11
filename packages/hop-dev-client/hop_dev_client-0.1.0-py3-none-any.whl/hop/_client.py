from typing import TYPE_CHECKING

import boto3
import os

from authlib.integrations.httpx_client import OAuth2Client
from ._utilities import Session

from ._exceptions import HopError
from httpx import URL


class Hop:
    _client: OAuth2Client

    @classmethod
    def startSession(
        cls,
        base_url: str | URL | None = None,
        token_endpoint: str | URL | None = None,
        client_id: str | None = None,
        client_secret: str | None = None,
    ):
        """
        Authenticate with hop and receive and Session Object

        :param str base_url: The base URL of your Hop instance,
            can be provided using the environment variable HOP_BASE_URL

        :param str token_endpoint: The full url of the OAuth 2 token endpoint,
            can be provided using the environment variable HOP_OAUTH_URL
        :param str client_id: The client ID used for client_credential auth,
            can be provided using the environment variable HOP_CLIENT_ID
        :param str client_secret: The client secret used for client_credential auth,
            can be provided using the environment variable HOP_CLIENT_SECRET

        :returns Session Object after Authentication

        """
        if base_url is None:
            base_url = os.environ.get("HOP_BASE_URL")
        if base_url is None:
            base_url = "https://api.dev.aquiva.hop.dev"
            base_url = base_url

        if token_endpoint is None:
            token_endpoint = os.environ.get("HOP_OAUTH_URL")
        if token_endpoint is None:
            token_endpoint = "https://auth.dev.aquiva.hop.dev/oauth2/token"

        if client_id is None:
            client_id = os.environ.get("HOP_CLIENT_ID")
        if client_id is None:
            raise HopError(
                "The client_id client option must be set either by passing\
client_id to the client or by setting the HOP_CLIENT_ID environment variable"
            )

        if client_secret is None:
            client_secret = os.environ.get("HOP_CLIENT_SECRET")
        if client_secret is None:
            raise HopError(
                "The client_secret client option must be set either by passing\
client_secret to the client or by setting the HOP_CLIENT_SECRET environment variable"
            )

        cls._client = OAuth2Client(
            client_id,
            client_secret,
            token_endpoint_auth_method="client_secret_basic",
        )
        response = cls._client.fetch_token(
            token_endpoint, grant_type="client_credentials"
        )

        session = Session()
        session.set_access_token(response["access_token"])
        session.base_url = base_url

        return session
