# https://developers.google.com/identity/openid-connect/openid-connect?hl=ja#discovery

# OAUTH2_ENDPOINT = "https://accounts.google.com/o/oauth2/v2/auth"
from datetime import timedelta

import httpx
from loguru import logger
from redis import Redis

from ddd_py.auth_ctx.usecase import google_login

DISCOVERY_DOC_URL = "https://accounts.google.com/.well-known/openid-configuration"
CACHE_KEY_DOC = "discovery_doc_google"
CACHE_KEY_TOKEN_ENDPOINT = "token_endpoint_google"
CACHE_EXPIRE = timedelta(days=30)

CLIENT_ID = "dummy"
CLIENT_SECRET = "dummy"
REDIRECT_URI = "http://localhost"


class PortImpl(google_login.Port):
    def __init__(self, http_client: httpx.AsyncClient, cache: Redis) -> None:
        self.http_client = http_client
        self.cache = cache

    async def code2token(self, code: str) -> google_login.IdpTokenResponse:
        endpoint: str | None = await self.cache.get(CACHE_KEY_TOKEN_ENDPOINT)
        if endpoint is None:
            doc = httpx.get(DISCOVERY_DOC_URL)
            if doc.status_code != 200:
                raise RuntimeError("Failed to get discovery doc")

            endpoint = doc.json()["token_endpoint"]

            if not self.cache.set(CACHE_KEY_DOC, doc.content, ex=CACHE_EXPIRE):
                raise RuntimeError("Failed to set cache")
            if not self.cache.set(CACHE_KEY_TOKEN_ENDPOINT, endpoint, ex=CACHE_EXPIRE):
                raise RuntimeError("Failed to set cache")

        body = {
            "code": code,
            "client_id": CLIENT_ID,
            "client_secret": CLIENT_SECRET,
            "redirect_uri": REDIRECT_URI,
            "grant_type": "authorization_code",
        }

        resp = await self.http_client.post(url=endpoint, data=body)
        if resp.status_code != 200:
            logger.info(
                f"Failed to get token from [{endpoint}]. \nstatus code: {resp.status_code}"
            )

            if resp.status_code == 404:
                logger.info("Trying one more after re-fetching discovery document...")
                doc_2 = httpx.get(DISCOVERY_DOC_URL)
                if doc_2.status_code != 200:
                    raise RuntimeError("Failed to get discovery doc")
                endpoint_2 = doc.json()["token_endpoint"]
                resp = await self.http_client.post(url=endpoint_2, data=body)
                if resp.status_code != 200:
                    raise RuntimeError("Failed to get token")
            else:
                raise RuntimeError("Failed to get token")

        id_token: str = resp.json()["id_token"]
        # TODO: verify id_token

        return google_login.IdpTokenResponse("")
