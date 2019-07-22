from fixtures import user, client, configed_app, login, logout, post


def test_logged_user_can_access_account(user, client, configed_app, login):
    with configed_app.test_request_context():
        response = login

        response = client.get("/account", follow_redirects=False)

    assert response.status_code == 200


def test_logged_user_can_access_logout(user, client, configed_app, login, logout):
    with configed_app.test_request_context():
        response = login
        response = logout

    assert response.status_code == 302


def test_logged_user_can_access_post_delete(user, client, configed_app, login, post):
    with configed_app.test_request_context():
        id = str(post.getId())
        response = login

        response = client.get("/post/" + id + "/delete", follow_redirects=False)

    assert response.status_code == 302


def test_logged_user_can_access_post_update(user, client, configed_app, login, post):
    with configed_app.test_request_context():
        id = str(post.getId())
        response = login

        response = client.get("/post/" + id + "/update", follow_redirects=False)

    assert response.status_code == 200


def test_logged_user_can_access_post_new(user, client, configed_app, login, post):
    with configed_app.test_request_context():
        id = str(post.getId())
        response = login

        response = client.get("/post/new", follow_redirects=False)

    assert response.status_code == 200


def test_logged_user_can_access_home_page(user, client, configed_app, login, post):
    with configed_app.test_request_context():
        id = str(post.getId())
        response = login

        response = client.get("/home", follow_redirects=False)

    assert response.status_code == 200


def test_logged_user_can_access_post_id(user, client, configed_app, login, post):
    with configed_app.test_request_context():
        id = str(post.getId())
        response = login

        response = client.get("/post/" + id, follow_redirects=False)

    assert response.status_code == 200


def test_logged_user_can_access_user_posts(user, client, configed_app, login, post):
    with configed_app.test_request_context():
        id = str(post.getId())
        response = login

        response = client.get("/user/test1", follow_redirects=False)

    assert response.status_code == 200
