import sys

sys.path.append("../")
from flaskblog import app


def test_unlogged_user_redirects_to_login_when_accesing_account():
    app.config["WTF_CSRF_ENABLED"] = False
    with app.test_request_context():
        tester = app.test_client()
        response = tester.get("/account", follow_redirects=True)

    assert b"Please log in to access this page." in response.data


@pytest.fixture
def test_xdelete():
    User.query.filter_by(email=dummy_user.email).delete()


def register_a_random_user(create_a_random_user):
    app.config["WTF_CSRF_ENABLED"] = False

    user = create_a_random_user

    with app.test_request_context():
        tester = app.test_client()
        response = tester.post(
            "/register",
            data=dict(
                username=user.username,
                email=user.email,
                password=user.password,
                confirm_password=user.password,
            ),
            follow_redirects=True,
        )
    assert b"Account created" in response.data
    assert response.status_code == 200
    return user
