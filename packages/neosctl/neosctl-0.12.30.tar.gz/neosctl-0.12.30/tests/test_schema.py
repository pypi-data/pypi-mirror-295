from unittest import mock

import pytest

from neosctl import schema


@pytest.fixture
def env():
    return schema.Env(
        name="env",
        hub_api_url="hub",
        user="env-user",
        access_token="env-access-token",
        refresh_token="env-refresh-token",
        ignore_tls=True,
        active=True,
        account="env-account",
        cores={},
    )


@pytest.fixture
def profile():
    return schema.Profile(
        gateway_api_url="gateway",
        storage_api_url="storage",
        hub_api_url="hub",
        user="profile-user",
        access_token="profile-access-token",
        refresh_token="profile-refresh-token",
        ignore_tls=True,
        account="profile-account",
    )


@pytest.fixture
def common_factory():
    def factory(active_env=None, profile=None):
        return schema.Common(
            profile_name="default",
            config=mock.Mock(),
            env={},
            credential=mock.Mock(),
            active_env=active_env,
            active_core=None,
            profile=profile,
        )

    return factory


def test_common_name_env(common_factory, env):
    common = common_factory(active_env=env)

    assert common.name == "env"


def test_common_name_default(common_factory):
    common = common_factory()

    assert common.name == "default"


def test_common_account_profile(common_factory, profile):
    common = common_factory(profile=profile)

    assert common.account == "profile-account"


def test_common_account_env(common_factory, env):
    common = common_factory(active_env=env)

    assert common.account == "env-account"


def test_common_account_default(common_factory):
    common = common_factory()

    assert common.account == "root"


def test_common_access_token_profile(common_factory, profile):
    common = common_factory(profile=profile)

    assert common.access_token == "profile-access-token"


def test_common_access_token_env(common_factory, env):
    common = common_factory(active_env=env)

    assert common.access_token == "env-access-token"


def test_common_access_token_default(common_factory):
    common = common_factory()

    assert common.access_token == ""


def test_common_refresh_token_profile(common_factory, profile):
    common = common_factory(profile=profile)

    assert common.refresh_token == "profile-refresh-token"


def test_common_refresh_token_env(common_factory, env):
    common = common_factory(active_env=env)

    assert common.refresh_token == "env-refresh-token"


def test_common_refresh_token_default(common_factory):
    common = common_factory()

    assert common.refresh_token == ""


def test_common_ignore_tls_profile(common_factory, profile):
    common = common_factory(profile=profile)

    assert common.ignore_tls is True


def test_common_ignore_tls_env(common_factory, env):
    common = common_factory(active_env=env)

    assert common.ignore_tls is True


def test_common_ignore_tls_default(common_factory):
    common = common_factory()

    assert common.ignore_tls is False


def test_core_handles_toml_null():
    c = schema.Core(name="name", host="host", account="null", active=True)

    assert c.account is None
