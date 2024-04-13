# https://developers.google.com/identity/openid-connect/openid-connect?hl=ja#discovery

# OAUTH2_ENDPOINT = "https://accounts.google.com/o/oauth2/v2/auth"
from datetime import timedelta

import httpx
from redis import Redis

from ddd_py.auth_ctx.usecase import google_login

DISCOVERY_DOC_URL = "https://accounts.google.com/.well-known/openid-configuration"
CACHE_KEY_DOC = "discovery_doc_google"
CACHE_KEY_AUTH_ENDPOINT = "authorization_endpoint_google"
CACHE_EXPIRE = timedelta(days=60)


class PortImpl(google_login.Port):
    def __init__(self, http_client: httpx.AsyncClient, cache_db: Redis) -> None:
        self.http_client = http_client
        self.cache_db = cache_db

    async def code2token(self, code: str) -> google_login.IdpTokenResponse:
        endpoint: str | None = await self.cache_db.get(CACHE_KEY_AUTH_ENDPOINT)
        if endpoint is None:
            doc = httpx.get(DISCOVERY_DOC_URL)
            if doc.status_code != 200:
                raise RuntimeError("Failed to get discovery doc")

            endpoint = doc.json()["authorization_endpoint"]

            if not self.cache_db.set(CACHE_KEY_DOC, doc.content, ex=CACHE_EXPIRE):
                raise RuntimeError("Failed to set cache")
            if not self.cache_db.set(
                CACHE_KEY_AUTH_ENDPOINT, endpoint, ex=CACHE_EXPIRE
            ):
                raise RuntimeError("Failed to set cache")

        # TODO:

        return google_login.IdpTokenResponse("")
