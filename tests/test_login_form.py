from fixtures import configed_app, user, client


def test_login_succesful_for_valid_credentials(configed_app, user, client):
    with configed_app.test_request_context():
        response = client.post(
            "login",
            data=dict(email=user.email, password=user.password),
            follow_redirects=False,
        )
    assert response.status_code == 302, (
        "User didn't logged in with valid credentials. Status code: "
        + str(response.status_code)
    )


def test_login_unsuccesful_for_incorrect_password(configed_app, user, client):
    with configed_app.test_request_context():
        response = client.post(
            "login",
            data=dict(email=user.email, password=user.password + "a"),
            follow_redirects=False,
        )
    assert response.status_code == 200, (
        "User logged in with incorrect password. Status code: "
        + str(response.status_code)
    )


def test_login_unsuccesful_for_incorrect_email(configed_app, user, client):
    with configed_app.test_request_context():
        response = client.post(
            "login",
            data=dict(email=user.email + "a", password=user.password),
            follow_redirects=False,
        )
    assert (
        response.status_code == 200
    ), "User logged in with incorrect email. Status code: " + str(response.status_code)


def test_login_unsuccesful_for_incorrect_email_format(configed_app, user, client):
    with configed_app.test_request_context():
        response = client.post(
            "login",
            data=dict(email=user.username, password=user.password),
            follow_redirects=False,
        )
    assert response.status_code == 200, (
        "User logged in with incorrect email format. Status code: "
        + str(response.status_code)
    )


def test_login_unsuccesful_for_missing_fields(configed_app, user, client):
    with configed_app.test_request_context():
        response = client.post(
            "login", data=dict(email="", password=""), follow_redirects=False
        )
    assert (
        response.status_code == 200
    ), "User logged in with missing fields. Status code: " + str(response.status_code)
