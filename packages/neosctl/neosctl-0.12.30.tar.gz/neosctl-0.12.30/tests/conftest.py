import configparser
import re
import textwrap
import typing

import click
import pytest
import rtoml
import typer.testing

import neosctl.cli


class CliRunner(typer.testing.CliRunner):
    target = neosctl.cli.app
    result = None

    _exclude_prints: typing.ClassVar = [
        "H000",
        "G003",
        "Can not find file",
        "Profile not found",
        "Enter password",
        "You need to login",
        "Invalid schema file",
        "Sorry",
    ]

    def invoke(self, *args, **kwargs):
        result = super().invoke(self.target, *args, **kwargs)
        self.result = result
        if result.exception:
            if isinstance(result.exception, SystemExit):
                # The error is already properly handled. Print it and return.
                no_print = any(exclude_rule in result.output for exclude_rule in self._exclude_prints)
                if not no_print:
                    pass
            else:
                raise result.exception.with_traceback(result.exc_info[2])
        return result

    def _clean_output(self, text: str):
        output = text.encode("ascii", errors="ignore").decode()
        output = re.sub(r"\s+\n", "\n", output)
        return textwrap.dedent(output).strip()

    def assert_output(self, expected):
        assert self._clean_output(self.result.output) == self._clean_output(expected)

    def assert_output_contains(self, expected):
        clean_output = self._clean_output(self.result.output)
        assert self._clean_output(expected) in clean_output, clean_output


@pytest.fixture
def cli_runner():
    return CliRunner()


class FakeContext:
    def __eq__(self, other: object) -> bool:
        return isinstance(other, click.Context)


@pytest.fixture(autouse=True)
def root_filepath(tmp_path, monkeypatch):
    root_fp = tmp_path / ".neosctl"
    monkeypatch.setattr("neosctl.util.constant.ROOT_FILEPATH", root_fp)

    return root_fp


@pytest.fixture(autouse=True)
def profile_filepath(tmp_path, monkeypatch):
    profile_fp = tmp_path / ".neosctl" / "profile"
    monkeypatch.setattr("neosctl.util.constant.PROFILE_FILEPATH", profile_fp)

    return profile_fp


@pytest.fixture(autouse=True)
def env_filepath(tmp_path, monkeypatch):
    env_fp = tmp_path / ".neosctl" / "env"
    monkeypatch.setattr("neosctl.util.constant.ENV_FILEPATH", env_fp)

    return env_fp


@pytest.fixture(autouse=True)
def credential_filepath(tmp_path, monkeypatch):
    credential_fp = tmp_path / ".neosctl" / "credential"
    monkeypatch.setattr("neosctl.util.constant.CREDENTIAL_FILEPATH", credential_fp)

    return credential_fp


@pytest.fixture(autouse=True)
def log_filepath(tmp_path, monkeypatch):
    log_fp = tmp_path / ".neosctl" / "error.log"
    monkeypatch.setattr("neosctl.util.constant.LOG_FILEPATH", log_fp)

    return log_fp


@pytest.fixture
def profile_dotfile_from_string_factory(profile_filepath, root_filepath):
    def factory(*args, legacy=False):
        c = configparser.ConfigParser()
        c.read_string(args[0])

        if legacy:
            with root_filepath.open("w") as profile_file:
                c.write(profile_file)
        else:
            root_filepath.mkdir(exist_ok=True)
            with profile_filepath.open("w") as profile_file:
                c.write(profile_file)

        return c

    return factory


@pytest.fixture
def profile_dotfile_factory(profile_filepath, root_filepath):
    def factory(*, legacy=False, **kwargs):
        c = configparser.ConfigParser()
        c.read_dict(
            {
                "default": {
                    "gateway_api_url": kwargs.get("gateway_api_url", "https://core-gateway/api/gateway"),
                    "registry_api_url": kwargs.get("registry_api_url", "https://registry/api/registry"),
                    "iam_api_url": kwargs.get("iam_api_url", "https://hub-host/api/iam"),
                    "storage_api_url": kwargs.get("storage_api_url", "https://storage/api/storage"),
                    "user": kwargs.get("user", "some-user"),
                    "access_token": kwargs.get("access_token", ""),
                    "refresh_token": kwargs.get("refresh_token", "some-refresh-token"),
                    "ignore_tls": kwargs.get("ignore_tls", False),
                },
            },
        )

        if legacy:
            with root_filepath.open("w") as profile_file:
                c.write(profile_file)
        else:
            root_filepath.mkdir(exist_ok=True)
            with profile_filepath.open("w") as profile_file:
                c.write(profile_file)

        return c

    return factory


@pytest.fixture
def env_dotfile_factory(env_filepath, root_filepath):
    def factory(envs):
        root_filepath.mkdir(exist_ok=True)
        with env_filepath.open("w") as env_file:
            rtoml.dump(envs, env_file)

        return envs

    return factory


@pytest.fixture(autouse=True)
def env_dotfile(request, env_dotfile_factory):
    if "nodotfile_patch" in request.keywords:
        return None

    envs = {
        "test": {
            "hub_api_url": "https://hub",
            "user": "some-username",
            "access_token": "",
            "refresh_token": "",
            "ignore_tls": False,
            "active": False,
            "account": "root",
            "cores": {},
        },
    }
    return env_dotfile_factory(envs)


@pytest.fixture
def active_env_dotfile(env_dotfile_factory):
    envs = {
        "test": {
            "hub_api_url": "https://hub-host/api/hub",
            "user": "some-username",
            "access_token": "access-token",
            "refresh_token": "refresh-token",
            "ignore_tls": False,
            "active": True,
            "account": "root",
            "cores": {},
        },
    }
    return env_dotfile_factory(envs)


@pytest.fixture
def active_env_core_dotfile(env_dotfile_factory):
    envs = {
        "test": {
            "hub_api_url": "https://hub",
            "user": "some-username",
            "access_token": "access-token",
            "refresh_token": "refresh-token",
            "ignore_tls": False,
            "active": True,
            "account": "root",
            "cores": {
                "smartconstruction": {
                    "name": "smartconstruction",
                    "host": "https://core",
                    "active": True,
                    "account": "sc",
                },
            },
        },
    }
    return env_dotfile_factory(envs)


@pytest.fixture(autouse=True)
def profile_dotfile(request, profile_dotfile_factory):
    if "nodotfile_patch" in request.keywords:
        return None
    return profile_dotfile_factory()
