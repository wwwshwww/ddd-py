# https://developers.google.com/identity/openid-connect/openid-connect?hl=ja#discovery

# OAUTH2_ENDPOINT = "https://accounts.google.com/o/oauth2/v2/auth"
import json
from base64 import b64decode
from datetime import timedelta
from typing import Any

import httpx
from loguru import logger
from redis import Redis

from ddd_py.auth_ctx.usecase import google_login

DISCOVERY_DOC_URL = "https://accounts.google.com/.well-known/openid-configuration"
CACHE_KEY_DOC = "discovery_doc_google"
CACHE_EXPIRE = timedelta(days=30)

CLIENT_ID = "dummy"
CLIENT_SECRET = "dummy"
REDIRECT_URI = "http://localhost"


class PortImpl(google_login.Port):
    def __init__(self, http_client: httpx.AsyncClient, cache: Redis) -> None:
        self.http_client = http_client
        self.cache = cache

    async def code2token(self, code: str) -> google_login.IdpTokenResponse:
        c: bytes | None = await self.cache.get(CACHE_KEY_DOC)
        doc: dict[str, Any]
        if c is not None:
            doc = json.loads(c)
        else:
            doc_resp = await self.http_client.get(DISCOVERY_DOC_URL)
            if doc_resp.status_code != 200:
                raise RuntimeError("Failed to get discovery doc")
            if not self.cache.set(CACHE_KEY_DOC, doc_resp.content, ex=CACHE_EXPIRE):
                raise RuntimeError("Failed to set cache")
            doc = doc_resp.json()

        token_endpoint: str = doc["token_endpoint"]

        body = {
            "code": code,
            "client_id": CLIENT_ID,
            "client_secret": CLIENT_SECRET,
            "redirect_uri": REDIRECT_URI,
            "grant_type": "authorization_code",
        }

        resp = await self.http_client.post(url=token_endpoint, data=body)
        if resp.status_code != 200:
            logger.info(
                f"Failed to get token from [{token_endpoint}]. \nstatus code: {resp.status_code}"
            )

            if resp.status_code == 404:
                logger.info("Trying one more after re-fetching discovery document...")
                doc_resp = await self.http_client.get(DISCOVERY_DOC_URL)
                if doc_resp.status_code != 200:
                    raise RuntimeError("Failed to get discovery doc")
                if not self.cache.set(CACHE_KEY_DOC, doc_resp.content, ex=CACHE_EXPIRE):
                    raise RuntimeError("Failed to set cache")

                resp = await self.http_client.post(url=token_endpoint, data=body)
                if resp.status_code != 200:
                    raise RuntimeError("Failed to get token")
            else:
                raise RuntimeError("Failed to get token")

        jwt: str = resp.json()["id_token"]
        jwt_header, jwt_payload, jwt_sig = jwt.split(".")
        # TODO: verify payload
        payload: dict[str, Any] = json.loads(b64decode(jwt_payload))

        return google_login.IdpTokenResponse(sub=payload["sub"])
