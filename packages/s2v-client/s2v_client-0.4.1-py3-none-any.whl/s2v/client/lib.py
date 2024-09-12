import abc
import datetime
import io
import os
import pathlib
import tempfile
import zipfile
from collections.abc import Callable
from typing import IO, Literal

import httpx
from google.auth import credentials, external_account, impersonated_credentials
from google.auth.transport import requests
from typing_extensions import Self

from s2v.version import version


def _google_auth(
    source_credentials: credentials.Credentials, audience: str
) -> Callable[[httpx.Request], httpx.Request]:
    if isinstance(source_credentials, external_account.Credentials):
        # External account credentials are not supported in the IDTokenCredentials directly yet.
        # See https://github.com/googleapis/google-auth-library-python/issues/1252
        source_credentials = source_credentials._initialize_impersonated_credentials()  # noqa: SLF001

    id_token_credentials = impersonated_credentials.IDTokenCredentials(source_credentials, audience, include_email=True)
    transport = requests.Request()

    def authenticate(request: httpx.Request) -> httpx.Request:
        id_token_credentials.before_request(transport, request.method, request.url, request.headers)
        return request

    return authenticate


def _zip_directory_contents(dir: pathlib.PurePath, target: IO[bytes]) -> None:
    """
    Creates a ZIP archive of the given directory's contents, recursively.

    :param dir: the directory to search for contents to be zipped
    :param target: a target IO to write the ZIP archive to
    """

    with zipfile.ZipFile(target, "w", compression=zipfile.ZIP_DEFLATED) as zip_file:
        for directory_name, _, files in os.walk(dir):
            directory = pathlib.PurePath(directory_name)
            zip_file.write(directory, directory.relative_to(dir))
            for file_name in files:
                file = directory / file_name
                zip_file.write(file, file.relative_to(dir))


class S2VError(Exception):
    def __init__(self, message: str) -> None:
        super().__init__(message)
        self.message = message

    def __str__(self) -> str:
        return self.message


class ValidationResult(abc.ABC):
    @abc.abstractmethod
    def __bool__(self) -> bool: ...


class ValidationSuccess(ValidationResult):
    def __bool__(self) -> Literal[True]:
        return True

    def __str__(self) -> str:
        return "OK"


class ValidationFailure(ValidationResult):
    def __init__(self, details: list[str]) -> None:
        self.details = details

    def __bool__(self) -> Literal[False]:
        return False

    def __str__(self) -> str:
        return "\n".join(self.details)


class S2VClient:
    def __init__(self, client: httpx.Client):
        self._httpx_client = client

    @classmethod
    def create(cls, base_url: str | httpx.URL, creds: credentials.Credentials | None) -> Self:
        authorization = _google_auth(creds, str(base_url)) if creds else None
        headers = {"User-Agent": f"s2v-client/{version}"}
        timeout = httpx.Timeout(timeout=datetime.timedelta(minutes=1).total_seconds())
        return cls(httpx.Client(base_url=base_url, auth=authorization, headers=headers, timeout=timeout))

    def validate(self, input_dir: pathlib.PurePath) -> ValidationResult:
        with tempfile.TemporaryFile(suffix=".zip") as zip_file:
            _zip_directory_contents(input_dir, zip_file)
            zip_file.seek(0)

            response = self._httpx_client.post(
                "/v1/validate",
                content=zip_file,
                headers={"Accept": "text/plain", "Accept-Encoding": "gzip", "Content-Type": "application/zip"},
            )

        match response.status_code:
            case httpx.codes.OK:
                return ValidationSuccess()
            case httpx.codes.UNPROCESSABLE_ENTITY:
                return ValidationFailure(response.text.splitlines())
            case _:
                response.raise_for_status()
                # This is unreachable, because raise_for_status() will already raise an error.
                # However, we need to convince the type checker that no return statement is missing.
                raise  # noqa: PLE0704

    def generate(self, input_dir: pathlib.PurePath, output_dir: pathlib.PurePath) -> ValidationResult:
        with tempfile.TemporaryFile(suffix=".zip") as request_data:
            _zip_directory_contents(input_dir, request_data)
            request_data.seek(0)

            response = self._httpx_client.post(
                "/v1/generate",
                content=request_data,
                headers={"Accept": "application/zip", "Content-Type": "application/zip"},
            )

        match response.status_code:
            case httpx.codes.OK:
                with zipfile.ZipFile(io.BytesIO(response.content), "r") as response_zip:
                    response_zip.extractall(output_dir)
                return ValidationSuccess()
            case httpx.codes.UNPROCESSABLE_ENTITY:
                return ValidationFailure(response.text.splitlines())
            case _:
                response.raise_for_status()
                # This is unreachable, because raise_for_status() will already raise an error.
                # However, we need to convince the type checker that no return statement is missing.
                raise  # noqa: PLE0704
