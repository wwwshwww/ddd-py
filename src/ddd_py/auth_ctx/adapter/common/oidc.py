from typing import TypedDict


class DiscoveryDocument(TypedDict):
    """
    Example:
    ```JSON
    {
        "issuer": "https://accounts.google.com",
        "authorization_endpoint": "https://accounts.google.com/o/oauth2/v2/auth",
        "device_authorization_endpoint": "https://oauth2.googleapis.com/device/code",
        "token_endpoint": "https://oauth2.googleapis.com/token",
        "userinfo_endpoint": "https://openidconnect.googleapis.com/v1/userinfo",
        "revocation_endpoint": "https://oauth2.googleapis.com/revoke",
        "jwks_uri": "https://www.googleapis.com/oauth2/v3/certs",
        "response_types_supported": [
            "code",
            "token",
            "id_token",
            "code token",
            "code id_token",
            "token id_token",
            "code token id_token",
            "none"
        ],
        "subject_types_supported": [
            "public"
        ],
        "id_token_signing_alg_values_supported": [
            "RS256"
        ],
        "scopes_supported": [
            "openid",
            "email",
            "profile"
        ],
        "token_endpoint_auth_methods_supported": [
            "client_secret_post",
            "client_secret_basic"
        ],
        "claims_supported": [
            "aud",
            "email",
            "email_verified",
            "exp",
            "family_name",
            "given_name",
            "iat",
            "iss",
            "locale",
            "name",
            "picture",
            "sub"
        ],
        "code_challenge_methods_supported": [
            "plain",
            "S256"
        ]
    }
    ```
    """

    issuer: str
    authorization_endpoint: str
    token_endpoint: str
    userinfo_endpoint: str
    jwks_uri: str
    registration_endpoint: str
    scopes_supported: list[str]
    response_types_supported: list[str]
    response_modes_supported: list[str]
    grant_types_supported: list[str]
    acr_values_supported: list[str]
    subject_types_supported: list[str]
    id_token_signing_alg_values_supported: list[str]
    userinfo_signing_alg_values_supported: list[str]
    request_object_signing_alg_values_supported: list[str]
    token_endpoint_auth_methods_supported: list[str]
    token_endpoint_auth_signing_alg_values_supported: list[str]
    display_values_supported: list[str]
    claim_types_supported: list[str]
    claims_supported: list[str]
    service_documentation: str
    claims_locales_supported: list[str]
    ui_locales_supported: list[str]
    claims_parameter_supported: bool
    request_parameter_supported: bool
    request_uri_parameter_supported: bool
    require_request_uri_registration: bool
    op_policy_uri: str
    op_tos_uri: str


class JWK(TypedDict):
    """
    JSON Web Key (JWK) is a JSON data structure that represents cryptographic keys.
    Examples:
    ```JSON
    {
        "kty": "RSA",
        "use": "sig",
        "kid": "1b94c",
        "alg": "RS256",
        "n": "0vx7agoebGcQSuuPiLJXZptN9nndrQmbXEg...",
        "e": "AQAB"
    },{
        "kty": "EC",
        "use": "sig",
        "kid": "e9bc097a-ce51-4036-9562-d2ade882db0d",
        "alg": "ES256",
        "crv": "P-256",
        "x": "MKBCTNIcKUSDii11ySs3526iDZ8AiTo7Tu6KPAqv7D4",
        "y": "4Etl6SRW2ji29vN8XRI7H6x6a8ZXoaRAFhzFU9C8mHyg"
    }
    ```
    """

    kty: str
    kid: str
    use: str
    alg: str
    n: str
    e: str
    x: str
    y: str
    crv: str


class JWKS(TypedDict):
    keys: list[JWK]
