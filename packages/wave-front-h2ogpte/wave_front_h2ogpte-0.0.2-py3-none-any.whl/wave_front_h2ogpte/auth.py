import datetime
import ssl
from typing import Optional

import httpx
from h2o_authn import TokenProvider, token
from h2o_authn.error import TokenEndpointError
from h2o_authn.provider import (DEFAULT_EXPIRES_IN_FALLBACK,
                                DEFAULT_EXPIRY_THRESHOLD, DEFAULT_HTTP_TIMEOUT)

DEFAULT_TOKEN_FAIL_RETRY_MAX_COUNT: int = 3


class ExtendedTokenProvider(TokenProvider):

    def __init__(
            self,
            *,
            client_id: str,
            username: str = None,
            password: str = None,
            issuer_url: Optional[str] = None,
            token_endpoint_url: Optional[str] = None,
            client_secret: Optional[str] = None,
            scope: Optional[str] = None,
            expiry_threshold: datetime.timedelta = DEFAULT_EXPIRY_THRESHOLD,
            expires_in_fallback: datetime.timedelta = DEFAULT_EXPIRES_IN_FALLBACK,
            http_timeout: datetime.timedelta = DEFAULT_HTTP_TIMEOUT,
            minimal_refresh_period: Optional[datetime.timedelta] = None,
            http_ssl_context: Optional[ssl.SSLContext] = None,
            token_generation_retry_max_count: Optional[
                int
            ] = DEFAULT_TOKEN_FAIL_RETRY_MAX_COUNT,
    ) -> None:
        self.token_generation_retry_max_count = token_generation_retry_max_count
        self.token_generation_retry_count = token_generation_retry_max_count

        self._username = username
        self._password = password

        # Need to initialize the parent first, to call
        # _ensure_token_endpoint_url() method
        self.init_parent(
            client_id,
            client_secret,
            expires_in_fallback,
            expiry_threshold,
            http_ssl_context,
            http_timeout,
            issuer_url,
            minimal_refresh_period,
            scope,
            token_endpoint_url,
        )
        self._ensure_token_endpoint_url()

        # Update parent class with the refresh token
        refresh_token = self._fetch_refresh_token_with_password()
        self.init_parent(
            client_id,
            client_secret,
            expires_in_fallback,
            expiry_threshold,
            http_ssl_context,
            http_timeout,
            issuer_url,
            minimal_refresh_period,
            scope,
            token_endpoint_url,
            refresh_token,
        )

    def init_parent(
            self,
            client_id,
            client_secret,
            expires_in_fallback,
            expiry_threshold,
            http_ssl_context,
            http_timeout,
            issuer_url,
            minimal_refresh_period,
            scope,
            token_endpoint_url,
            refresh_token="",
    ):
        super().__init__(
            refresh_token=refresh_token,
            client_id=client_id,
            issuer_url=issuer_url,
            token_endpoint_url=token_endpoint_url,
            client_secret=client_secret,
            scope=scope,
            expiry_threshold=expiry_threshold,
            expires_in_fallback=expires_in_fallback,
            http_timeout=http_timeout,
            minimal_refresh_period=minimal_refresh_period,
            http_ssl_context=http_ssl_context,
        )

    def _call_token_endpoint_with_password(self):
        with self._client() as client:
            resp = client.post(
                self._token_endpoint_url,
                data=self._create_password_grant_request_data(),
            )
        return resp

    def _fetch_refresh_token_with_password(self):
        resp = self._call_token_endpoint_with_password()
        resp_data = resp.json()

        try:
            resp.raise_for_status()
        except httpx.HTTPStatusError:
            if resp.status_code != 400 or not resp_data.get("error"):
                raise
            raise TokenEndpointError(
                error=resp_data["error"],
                error_description=resp_data.get("error_description"),
                error_uri=resp_data.get("error_uri"),
            ) from None

        return resp_data.get("refresh_token")

    def _create_password_grant_request_data(self):
        data = {
            "grant_type": "password",
            "client_id": self._client_id,
            "username": self._username,
            "password": self._password,
        }

        if self._client_secret:
            data["client_secret"] = self._client_secret

        if self._scope:
            data["scope"] = self._scope

        return data

    def token(self) -> token.Token:
        try:
            token = super().token()
            self.token_generation_retry_count = self.token_generation_retry_max_count
            return token
        except Exception as e:
            print(f"Token generation failed with the refresh grant!, {e}")
            self.token_generation_retry_count -= 1
            if self.token_generation_retry_count >= 0:
                print(f"Retrying with the password grant type...")
                resp = self._call_token_endpoint_with_password()
                self.token_generation_retry_count = (
                    self.token_generation_retry_max_count
                )
                self._update_token(resp)
