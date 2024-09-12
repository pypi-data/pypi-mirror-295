import pathlib
import stat
import typing
from collections.abc import Mapping
from contextlib import AbstractContextManager
from os import PathLike
from types import TracebackType
from typing import Any, Literal

import httpx
import msal.application
import msal.oauth2cli.oidc
import msal.token_cache
from google.auth import exceptions, external_account
from typing_extensions import Self


class FileTokenCache(msal.token_cache.SerializableTokenCache, AbstractContextManager["FileTokenCache"]):
    def __init__(self, path: pathlib.Path) -> None:
        super().__init__()
        self.path = path

    def __enter__(self) -> Self:
        if self.path.exists():
            with self.path.open() as f:
                self.deserialize(f.read())
        return self

    def __exit__(
        self, exc_type: type[BaseException] | None, exc_val: BaseException | None, exc_tb: TracebackType | None
    ) -> Literal[False]:
        if self.has_state_changed:
            self.path.parent.mkdir(parents=True, exist_ok=True)
            with self.path.open("w") as f:
                f.write(self.serialize())
            self.path.chmod(stat.S_IRUSR | stat.S_IWUSR)
        return False


class AzureCredentials(external_account.Credentials):
    def __init__(
        self,
        token_cache: msal.token_cache.TokenCache,
        credential_source: Mapping[str, Any],
        **kwargs: Any,
    ) -> None:
        super().__init__(credential_source=credential_source, **kwargs)

        self._app = msal.application.PublicClientApplication(self.entra_id_app_id, token_cache=token_cache)

    def _constructor_args(self) -> Mapping[str, Any]:
        args = super()._constructor_args()
        return {**args, "token_cache": self._app.token_cache}

    @property
    def entra_id_app_id(self) -> str:
        if not self._credential_source:
            msg = "'credential_source' is missing or empty"
            raise exceptions.MalformedError(msg)

        credential_src_url_str = self._credential_source.get("url")
        if not credential_src_url_str:
            msg = "'credential_source.url' is missing"
            raise exceptions.MalformedError(msg)

        credential_src_url = httpx.URL(credential_src_url_str)
        resource: str = credential_src_url.params.get("resource")
        if not resource:
            msg = "'credential_source.url' is missing the 'resource' parameter"
            raise exceptions.MalformedError(msg)

        try:
            resource_url = httpx.URL(resource)
        except (TypeError, httpx.InvalidURL) as err:
            msg = "'credential_source.url(resource)' parameter is malformed"
            raise exceptions.MalformedError(msg) from err

        return resource_url.host

    @property
    def entra_id_scopes(self) -> list[str]:
        impersonation_scope = f"{self.entra_id_app_id}/user_impersonation"
        return [impersonation_scope]

    def login(self) -> None:
        match self._app.acquire_token_interactive(
            scopes=self.entra_id_scopes, prompt=msal.oauth2cli.oidc.Prompt.CONSENT
        ):
            case {"error": error, "error_description": error_description}:
                msg = f"{error}: {error_description}"
                raise exceptions.OAuthError(msg)

    def retrieve_subject_token(self, _: Any) -> str:
        accounts = self._app.get_accounts()
        if not accounts:
            msg = "No logged in user account available."
            raise exceptions.RefreshError(msg)

        account = accounts[0]
        match self._app.acquire_token_silent(scopes=self.entra_id_scopes, account=account):
            case {"access_token": access_token} if isinstance(access_token, str):
                return access_token
            case {"error": error, "error_description": error_description}:
                msg = f"{error}: {error_description}"
                raise exceptions.RefreshError(msg)
            case _:
                msg = "Cannot parse token response"
                raise exceptions.MalformedError(msg)

    @classmethod
    def from_file(cls, filename: str | PathLike[str], **kwargs: Any) -> Self:
        return typing.cast(Self, super().from_file(filename, **kwargs))
