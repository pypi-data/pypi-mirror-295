import json
import os

import h2o_authn
import requests
from h2ogpte import H2OGPTE

from .auth import ExtendedTokenProvider


class RequestError(Exception):
    def __init__(self, message):
        self.message = message


class RemoteError(Exception):
    def __init__(self, message):
        self.message = message


def get_token_endpoint(issuer_url):
    # Call OIDC protocol standard url to retrieve token endpoint
    uri = issuer_url.rstrip("/") + "/.well-known/openid-configuration"

    res = requests.get(url=uri)
    try:
        res.raise_for_status()
    except requests.HTTPError as e:
        msg = f"Authentication server responded with {res.status_code}."
        print(f"[ERROR] {msg}\n\n{res.content}")
        raise RequestError(msg) from e

    try:
        response_json = res.json()
    except json.JSONDecodeError as e:
        msg = "Authentication server response is not a valid JSON."
        print(f"[ERROR] {msg}\n\n{res.content}")
        raise RequestError(msg) from e

    if "error" in response_json:
        raise RemoteError(response_json["error"])

    if "token_endpoint" in response_json:
        return response_json["token_endpoint"]
    else:
        raise Exception(
            f'Authentication endpoint discovery failed. {response_json["error"]}'
        )


def connect_to_h2ogpte(refresh_token):
    # Precedence given in the following order;
    # 1. If H2OGPTE_API_TOKEN is set, use it without a token provider
    # 2. If OIDC_AUTH_URL is set, use it to generate a refresh token
    # 3. If H2O_WAVE_OIDC_PROVIDER_URL is set, use it along with q.auth.refresh_token
    # 4. Or else raise an error
    gpte_api_token = os.getenv("H2OGPTE_API_TOKEN")

    if gpte_api_token:
        print(
            f"[H2O_GPTE_CLIENT] H2OGPTE_API_TOKEN found, trying to "
            f"connect to {os.getenv('H2OGPTE_URL')} using "
            f"H2OGPTE_API_TOKEN: {gpte_api_token[:5]}..."
            f"{gpte_api_token[-5:]}"
        )

        return H2OGPTE(
            address=os.getenv("H2OGPTE_URL"),
            api_key=os.getenv("H2OGPTE_API_TOKEN"),
        )

    else:
        if os.getenv("OIDC_AUTH_URL"):
            print(
                f"[H2O_GPTE_CLIENT] OIDC_AUTH_URL found, trying to "
                f"connect to {os.getenv('OIDC_AUTH_URL')} to generate "
                f"a refresh token..."
            )
            auth_url = os.getenv("OIDC_AUTH_URL")
            token_endpoint = get_token_endpoint(auth_url)

            client_id = os.getenv("OIDC_CLIENT_ID")
            client_secret = os.getenv("OIDC_CLIENT_SECRET")
            username = os.getenv("OIDC_USERNAME")
            password = os.getenv("OIDC_PASSWORD")

            client_secret_display = (
                f"{client_secret[:3]}...{client_secret[-3:]}"
                if client_secret is not None
                else ""
            )
            print(
                f"[H2O_GPTE_CLIENT] Generating a refresh_token with "
                f"token_endpoint: {token_endpoint} "
                f"client_id: {client_id} "
                f"{client_secret_display} "
                f"username: {username} "
                f"with password: {'*' * len(password)}..."
            )
            token_provider = ExtendedTokenProvider(
                username=username,
                password=password,
                token_endpoint_url=token_endpoint,
                client_id=client_id,
                client_secret=client_secret if client_secret else None,
            )
        elif refresh_token is not None:
            print(
                f"[H2O_GPTE_CLIENT] q.auth.refresh_token found, trying to "
                f"connect to {os.getenv('OIDC_PROVIDER_URL')}..."
            )
            token_endpoint = get_token_endpoint(os.getenv("OIDC_PROVIDER_URL"))
            client_id = os.getenv("OIDC_CLIENT_ID")
            client_secret = os.getenv("OIDC_CLIENT_SECRET")

            client_secret_display = (
                f"{client_secret[:3]}...{client_secret[-3:]}"
                if client_secret is not None
                else ""
            )
            print(
                f"[H2O_GPTE_CLIENT] Using token provider with "
                f"token_endpoint: {token_endpoint} "
                f"client_id: {client_id} "
                f"{client_secret_display} "
                f"with refresh_token: {refresh_token[:3]}...{refresh_token[-3:]}..."
            )
            token_provider = h2o_authn.TokenProvider(
                refresh_token=refresh_token,
                token_endpoint_url=token_endpoint,
                client_id=client_id,
                client_secret=client_secret if client_secret else None,
            )
        else:
            raise Exception(
                "You need to set one of H2OGPTE_API_TOKEN, "
                "OIDC_AUTH_URL or H2O_WAVE_OIDC_PROVIDER_URL"
            )
        return H2OGPTE(address=os.getenv("H2OGPTE_URL"), token_provider=token_provider)
