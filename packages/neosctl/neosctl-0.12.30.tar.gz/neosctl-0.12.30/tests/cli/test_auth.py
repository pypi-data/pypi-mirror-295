from tests.helper import render_cmd_output

GATEWAY_URL = "https://core-gateway/api/gateway"
IAM_URL = "https://hub-host/api/hub/iam"
LOGIN_URL = f"{IAM_URL}/login"
REFRESH_URL = f"{IAM_URL}/refresh"
LOGOUT_URL = f"{IAM_URL}/logout"


def test_login(cli_runner, httpx_mock):
    payload = {
        "access_token": "some-access-token",
        "refresh_token": "some-refresh-token",
        "expires_in": "300",
        "refresh_expires_in": "1800",
        "scope": "email profile",
        "token_type": "Bearer",
        "session_state": "some-session-state",
    }

    httpx_mock.add_response(
        method="POST",
        url=LOGIN_URL,
        json=payload,
    )

    result = cli_runner.invoke(["auth", "login"], input="some-pass\n")

    assert result.exit_code == 0
    assert "Login success" in result.output


def test_login_non_interactive(cli_runner, httpx_mock):
    payload = {
        "access_token": "some-access-token",
        "refresh_token": "some-refresh-token",
        "expires_in": "300",
        "refresh_expires_in": "1800",
        "scope": "email profile",
        "token_type": "Bearer",
        "session_state": "some-session-state",
    }

    httpx_mock.add_response(
        method="POST",
        url=LOGIN_URL,
        json=payload,
    )

    result = cli_runner.invoke(["auth", "login", "-p", "some-pass"])

    assert result.exit_code == 0
    assert "Login success" in result.output


def test_login_bad_credentials(cli_runner, httpx_mock):
    payload = {
        "type": "failed-authorization",
        "title": "Authorization failed.",
        "error": {
            "error": "invalid_grant",
            "error_description": "Invalid user credentials",
        },
    }

    httpx_mock.add_response(
        url=LOGIN_URL,
        json=payload,
        status_code=401,
    )

    result = cli_runner.invoke(["auth", "login"], input="some-pass\n")

    assert result.exit_code == 1
    assert (
        result.output
        == f"[default] Enter password for user (some-user): \n{render_cmd_output(payload, sort_keys=False)}"
    )


def test_login_bad_profile(cli_runner):
    result = cli_runner.invoke(["--profile=bad-profile", "auth", "login"], input="some-pass\n")

    assert result.exit_code == 1
    assert "Profile bad-profile not found." in result.output


def test_logout(cli_runner, httpx_mock):
    httpx_mock.add_response(
        method="POST",
        url=LOGOUT_URL,
        json={},
    )
    result = cli_runner.invoke(["auth", "logout"])

    assert result.exit_code == 0
    assert "Logout success" in result.output


def test_logout_bad_credentials(cli_runner, httpx_mock):
    payload = {
        "type": "failed-authorization",
        "title": "Authorization failed.",
        "error": {
            "error": "invalid_grant",
            "error_description": "Invalid user credentials",
        },
    }

    httpx_mock.add_response(
        url=LOGOUT_URL,
        json=payload,
        status_code=401,
    )

    result = cli_runner.invoke(["auth", "logout"])

    assert result.exit_code == 1
    assert result.output == render_cmd_output(payload, sort_keys=False)


def test_logout_bad_profile(cli_runner):
    result = cli_runner.invoke(["--profile=bad-profile", "auth", "logout"])

    assert result.exit_code == 1
    assert "Profile bad-profile not found." in result.output
