# https://developers.google.com/identity/openid-connect/openid-connect?hl=ja#discovery

# OAUTH2_ENDPOINT = "https://accounts.google.com/o/oauth2/v2/auth"
import json
from base64 import b64decode
from datetime import timedelta
from typing import Any

import httpx
from loguru import logger
from redis import Redis

from ddd_py.auth_ctx.adapter.common.oidc import JWKS, DiscoveryDocument
from ddd_py.auth_ctx.usecase import google_login

DISCOVERY_DOC_URL = "https://accounts.google.com/.well-known/openid-configuration"
CACHE_KEY_DOC = "discovery_doc_google"
CACHE_KEY_JWKS = "jwk_uri_google"
CACHE_EXPIRE = timedelta(days=30)

CLIENT_ID = "dummy"
CLIENT_SECRET = "dummy"
REDIRECT_URI = "http://localhost"


class PortImpl(google_login.Port):
    def __init__(self, http_client: httpx.AsyncClient, cache: Redis) -> None:
        self.http_client = http_client
        self.cache = cache

    async def code2token(self, code: str) -> google_login.IdpTokenResponse:
        doc: DiscoveryDocument
        jwks: JWKS
        doc_cache: bytes | None = await self.cache.get(CACHE_KEY_DOC)
        jwks_cache: bytes | None = await self.cache.get(CACHE_KEY_JWKS)
        if (doc_cache is not None) and (jwks_cache is not None):
            doc = json.loads(doc_cache)
            jwks = json.loads(jwks_cache)
        else:
            doc, jwks = await self._refresh_discovery_doc()

        body = {
            "code": code,
            "client_id": CLIENT_ID,
            "client_secret": CLIENT_SECRET,
            "redirect_uri": REDIRECT_URI,
            "grant_type": "authorization_code",
        }

        resp = await self.http_client.post(url=doc["token_endpoint"], data=body)
        if resp.status_code != 200:
            logger.info(f"Failed to get token from {doc["token_endpoint"]}")

            if resp.status_code == 404:
                logger.info("Trying one more after re-fetching discovery document...")
                doc, jwks = await self._refresh_discovery_doc()

                resp = await self.http_client.post(url=doc["token_endpoint"], data=body)
                if resp.status_code != 200:
                    raise RuntimeError("Failed to get token")
            else:
                raise RuntimeError("Failed to get token")

        jwt: str = resp.json()["id_token"]
        jwt_header, jwt_payload, jwt_sig = jwt.split(".")
        # TODO: verify payload
        payload: dict[str, Any] = json.loads(b64decode(jwt_payload))

        return google_login.IdpTokenResponse(sub=payload["sub"])

    async def _refresh_discovery_doc(self) -> tuple[DiscoveryDocument, JWKS]:
        doc_resp = await self.http_client.get(DISCOVERY_DOC_URL)
        if doc_resp.status_code != 200:
            raise RuntimeError("Failed to get discovery doc")
        jwks_resp = await self.http_client.get(doc_resp.json()["jwks_uri"])
        if jwks_resp.status_code != 200:
            raise RuntimeError("Failed to get jwk")

        if not self.cache.set(CACHE_KEY_DOC, doc_resp.content, ex=CACHE_EXPIRE):
            raise RuntimeError("Failed to set cache")
        if not self.cache.set(CACHE_KEY_JWKS, jwks_resp.content, ex=CACHE_EXPIRE):
            raise RuntimeError("Failed to set cache")

        return doc_resp.json(), jwks_resp.json()
