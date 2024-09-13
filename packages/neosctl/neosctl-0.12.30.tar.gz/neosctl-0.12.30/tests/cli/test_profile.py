import pytest

from tests.helper import render_cmd_output


@pytest.mark.nodotfile_patch
def test_init_new_profile(cli_runner, profile_filepath):
    args = [
        "https://gateway",
        "https://hub",
        "https://storage",
        "some-username",
    ]
    # Add default profile
    result = cli_runner.invoke(
        ["profile", "init"],
        input="\n".join(args),
    )

    assert result.exit_code == 0

    config_file = """[default]
gateway_api_url = https://gateway
registry_api_url = 
iam_api_url = 
hub_api_url = https://hub
storage_api_url = https://storage
user = some-username
access_token = 
refresh_token = 
ignore_tls = False
account = root
http_proxy = 

"""

    with profile_filepath.open() as f:
        assert f.read() == config_file


def test_init_new_profile_non_interactive_required_args(cli_runner):
    # Add default profile
    result = cli_runner.invoke(
        ["profile", "init", "--non-interactive"],
    )

    assert result.exit_code == 1
    cli_runner.assert_output(
        r"""Initialising [default] profile.

Error: --hostname/-h and --username/-u required for non-interactive mode.
""",
    )


@pytest.mark.nodotfile_patch
def test_init_new_profile_non_interactive(cli_runner, profile_filepath):
    # Add default profile
    result = cli_runner.invoke(
        ["profile", "init", "-h", "https://test.domain", "-u", "username", "--non-interactive"],
    )

    assert result.exit_code == 0, result.output

    config_file = """[default]
gateway_api_url = https://test.domain/api/gateway
registry_api_url = 
iam_api_url = 
hub_api_url = https://test.domain/api/hub
storage_api_url = https://saas.test.domain
user = username
access_token = 
refresh_token = 
ignore_tls = False
account = root
http_proxy = 

"""

    with profile_filepath.open() as f:
        assert f.read() == config_file


@pytest.mark.nodotfile_patch
def test_init_new_profile_non_interactive_url_validation(cli_runner):
    # Add default profile
    result = cli_runner.invoke(
        ["profile", "init", "-h", "domain.com", "-u", "username", "--non-interactive"],
    )

    assert result.exit_code == 2  # noqa: PLR2004
    cli_runner.assert_output(
        r"""Initialising [default] profile.
Usage: neosctl profile init [OPTIONS]
Try 'neosctl profile init --help' for help.

 Error
 Invalid url, must match pattern: `re.compile('http[s]?:\\/\\/.*')`.
""",
    )


@pytest.mark.nodotfile_patch
def test_init_new_profile_from_hostname(cli_runner, profile_filepath):
    args = [
        "",
        "",
        "",
        "some-username",
    ]
    # Add default profile
    result = cli_runner.invoke(
        ["profile", "init", "-h", "https://test.domain"],
        input="\n".join(args),
    )

    assert result.exit_code == 0, result.output

    config_file = """[default]
gateway_api_url = https://test.domain/api/gateway
registry_api_url = 
iam_api_url = 
hub_api_url = https://test.domain/api/hub
storage_api_url = https://saas.test.domain
user = some-username
access_token = 
refresh_token = 
ignore_tls = False
account = root
http_proxy = 

"""

    with profile_filepath.open() as f:
        assert f.read() == config_file


def test_init_new_profile_ignore_tls(cli_runner, profile_filepath):
    args = [
        "https://gateway",
        "https://hub",
        "https://storage",
        "some-username",
    ]
    # Add default profile
    result = cli_runner.invoke(
        ["profile", "init", "--ignore-tls"],
        input="\n".join(args),
    )

    assert result.exit_code == 0

    config_file = """[default]
gateway_api_url = https://gateway
registry_api_url = 
iam_api_url = 
hub_api_url = https://hub
storage_api_url = https://storage
user = some-username
access_token = 
refresh_token = 
ignore_tls = True
account = root
http_proxy = 

"""

    with profile_filepath.open() as f:
        assert f.read() == config_file


def test_init_new_profile_account(cli_runner, profile_filepath):
    args = [
        "https://gateway",
        "https://hub",
        "https://storage",
        "some-username",
    ]
    # Add default profile
    result = cli_runner.invoke(
        ["profile", "init", "--account", "test"],
        input="\n".join(args),
    )

    assert result.exit_code == 0

    config_file = """[default]
gateway_api_url = https://gateway
registry_api_url = 
iam_api_url = 
hub_api_url = https://hub
storage_api_url = https://storage
user = some-username
access_token = 
refresh_token = 
ignore_tls = False
account = test
http_proxy = 

"""

    with profile_filepath.open() as f:
        assert f.read() == config_file


def test_init_new_profile_url_validation(cli_runner, profile_filepath):
    args = [
        "gateway",
        "https://gateway",
        "https://hub",
        "https://storage",
        "some-username",
    ]
    # Add default profile
    result = cli_runner.invoke(
        ["profile", "init"],
        input="\n".join(args),
    )

    assert result.exit_code == 0

    config_file = """[default]
gateway_api_url = https://gateway
registry_api_url = 
iam_api_url = 
hub_api_url = https://hub
storage_api_url = https://storage
user = some-username
access_token = 
refresh_token = 
ignore_tls = False
account = root
http_proxy = 

"""

    with profile_filepath.open() as f:
        assert f.read() == config_file


def test_init_new_profile_all_input_provided(cli_runner, profile_filepath):
    # Add default profile
    result = cli_runner.invoke(
        [
            "profile",
            "init",
            "-g",
            "https://gateway",
            "--hub-api-url",
            "https://hub",
            "-s",
            "https://storage",
            "-u",
            "some-username",
        ],
    )

    assert result.exit_code == 0

    config_file = """[default]
gateway_api_url = https://gateway
registry_api_url = 
iam_api_url = 
hub_api_url = https://hub
storage_api_url = https://storage
user = some-username
access_token = 
refresh_token = 
ignore_tls = False
account = root
http_proxy = 

"""

    with profile_filepath.open() as f:
        assert f.read() == config_file


def test_init_new_profile_all_input_provided_url_validation(cli_runner):
    # Add default profile
    result = cli_runner.invoke(
        [
            "profile",
            "init",
            "-g",
            "gateway",
            "--hub-api-url",
            "https://hub",
            "-s",
            "https://storage",
            "-u",
            "some-username",
        ],
    )

    assert result.exit_code == 2  # noqa: PLR2004
    cli_runner.assert_output(
        r"""Initialising [default] profile.
Usage: neosctl profile init [OPTIONS]
Try 'neosctl profile init --help' for help.

 Error

 Invalid url, must match pattern: `re.compile('http[s]?:\\/\\/.*')`.
""",
    )


def test_init_existing_profile(cli_runner, profile_filepath):
    args = [
        "",
        "",
        "",
        "other-username",
    ]
    # Add another profile
    result = cli_runner.invoke(["profile", "init"], input="\n".join(args))

    assert result.exit_code == 0, result.output

    config_file = """[default]
gateway_api_url = https://core-gateway/api/gateway
registry_api_url = 
iam_api_url = 
hub_api_url = https://hub-host/api/hub
storage_api_url = https://storage/api/storage
user = other-username
access_token = 
refresh_token = 
ignore_tls = False
account = root
http_proxy = 

"""

    with profile_filepath.open() as f:
        assert config_file == f.read()


def test_init_additional_profile(cli_runner, profile_filepath):
    args = [
        "https://gateway",
        "https://hub",
        "https://storage",
        "other-username",
    ]
    # Add another profile
    result = cli_runner.invoke(
        ["-p", "foo", "profile", "init"],
        input="\n".join(args),
    )

    assert result.exit_code == 0

    config_file = """[default]
gateway_api_url = https://core-gateway/api/gateway
registry_api_url = https://registry/api/registry
iam_api_url = https://hub-host/api/iam
storage_api_url = https://storage/api/storage
user = some-user
access_token = 
refresh_token = some-refresh-token
ignore_tls = False

[foo]
gateway_api_url = https://gateway
registry_api_url = 
iam_api_url = 
hub_api_url = https://hub
storage_api_url = https://storage
user = other-username
access_token = 
refresh_token = 
ignore_tls = False
account = root
http_proxy = 

"""

    with profile_filepath.open() as f:
        assert config_file == f.read()


def test_view(cli_runner, profile_dotfile):
    result = cli_runner.invoke(["profile", "view"])

    assert result.exit_code == 0
    assert result.output == render_cmd_output({**profile_dotfile["default"]})


def test_list(cli_runner):
    result = cli_runner.invoke(["profile", "list"])

    assert result.exit_code == 0
    assert (
        result.output
        == """[
  "default"
]

"""
    )


def test_credentials(cli_runner, credential_filepath):
    result = cli_runner.invoke(["profile", "credentials", "key", "secret"])

    assert result.exit_code == 0

    config_file = """[default]
access_key_id = key
secret_access_key = secret

"""

    with credential_filepath.open() as f:
        assert config_file == f.read()


def test_delete(cli_runner, profile_filepath):
    result = cli_runner.invoke(["profile", "delete"], input="y\n")

    assert result.exit_code == 0

    with profile_filepath.open() as f:
        assert not f.read()


def test_delete_unknown_profile(cli_runner):
    result = cli_runner.invoke(["-p", "foo", "profile", "delete"], input="y\n")

    assert result.exit_code == 1
    assert (
        result.output
        == """Remove [foo] profile [y/N]: y
Can not remove foo profile, profile not found.
"""
    )


def test_delete_abort(cli_runner, profile_filepath):
    result = cli_runner.invoke(["profile", "delete"], input="n\n")

    assert result.exit_code == 1

    with profile_filepath.open() as f:
        assert (
            f.read()
            == """[default]
gateway_api_url = https://core-gateway/api/gateway
registry_api_url = https://registry/api/registry
iam_api_url = https://hub-host/api/iam
storage_api_url = https://storage/api/storage
user = some-user
access_token = 
refresh_token = some-refresh-token
ignore_tls = False

"""
        )
