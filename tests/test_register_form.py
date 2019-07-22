from fixtures import new_user, delete_user, configed_app, client


def test_register_succesful_for_correct_credentials(new_user, configed_app, client):
    with configed_app.test_request_context():
        response = client.post(
            "register",
            data=dict(
                username=new_user.username,
                email=new_user.email,
                password=new_user.password,
                confirm_password=new_user.password,
            ),
            follow_redirects=False,
        )
    assert response.status_code == 302
    delete_user(new_user)


def test_register_unsuccesful_for_missing_confirm_password(
    new_user, configed_app, client
):
    with configed_app.test_request_context():
        response = client.post(
            "register",
            data=dict(
                username=new_user.username,
                email=new_user.email,
                password=new_user.password,
                confirm_password="",
            ),
            follow_redirects=False,
        )
    assert response.status_code == 200
    delete_user(new_user)


def test_register_unsuccesful_for_missing_password(new_user, configed_app, client):
    with configed_app.test_request_context():
        response = client.post(
            "register",
            data=dict(
                username=new_user.username,
                email=new_user.email,
                password="",
                confirm_password=new_user.password,
            ),
            follow_redirects=False,
        )
    assert response.status_code == 200
    delete_user(new_user)


def test_register_unsuccesful_for_missing_email(new_user, configed_app, client):
    with configed_app.test_request_context():
        response = client.post(
            "register",
            data=dict(
                username=new_user.username,
                email="",
                password=new_user.password,
                confirm_password=new_user.password,
            ),
            follow_redirects=False,
        )
    assert response.status_code == 200
    delete_user(new_user)


def test_register_unsuccesful_for_missing_username(new_user, configed_app, client):
    with configed_app.test_request_context():
        response = client.post(
            "register",
            data=dict(
                username="",
                email=new_user.email,
                password=new_user.password,
                confirm_password=new_user.password,
            ),
            follow_redirects=False,
        )
    assert response.status_code == 200
    delete_user(new_user)


def test_register_unsuccesful_for_big_username(new_user, configed_app, client):
    with configed_app.test_request_context():
        response = client.post(
            "register",
            data=dict(
                username="".join("a" for i in range(60)),
                email=new_user.email,
                password=new_user.password,
                confirm_password=new_user.password,
            ),
            follow_redirects=False,
        )
    assert response.status_code == 200
    delete_user(new_user)


def test_register_unsuccesful_for_different_pass_and_conf_pass(
    new_user, configed_app, client
):
    with configed_app.test_request_context():
        response = client.post(
            "register",
            data=dict(
                username=new_user.username,
                email=new_user.email,
                password=new_user.password,
                confirm_password=new_user.password + "a",
            ),
            follow_redirects=False,
        )
    assert response.status_code == 200
    delete_user(new_user)
