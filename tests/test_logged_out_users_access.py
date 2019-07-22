from fixtures import client, configed_app, logout, post, user


def test_logout_user_can_not_access_account(client, configed_app):
    with configed_app.test_request_context():

        response = client.get("/account", follow_redirects=False)

    assert response.status_code == 403


def test_logout_user_can_not_access_logout(client, configed_app, user, logout):
    with configed_app.test_request_context():
        response = logout

    assert response.status_code == 403


def test_logout_user_can_not_access_post_delete(client, configed_app, post):
    with configed_app.test_request_context():
        id = str(post.getId())

        response = client.get("/post/" + id + "/delete", follow_redirects=False)

    assert response.status_code == 403


def test_logout_user_can_not_access_post_update(client, configed_app, post):
    with configed_app.test_request_context():
        id = str(post.getId())

        response = client.get("/post/" + id + "/update", follow_redirects=False)

    assert response.status_code == 403


def test_logout_user_can_not_access_post_new(client, configed_app, post):
    with configed_app.test_request_context():
        id = str(post.getId())

        response = client.get("/post/new", follow_redirects=False)

    assert response.status_code == 403


def test_logout_user_can_access_home_page(client, configed_app, post):
    with configed_app.test_request_context():
        id = str(post.getId())

        response = client.get("/home", follow_redirects=False)

    assert response.status_code == 200


def test_logout_user_can_access_post_id(client, configed_app, post):
    with configed_app.test_request_context():
        id = str(post.getId())

        response = client.get("/post/" + id, follow_redirects=False)

    assert response.status_code == 200


def test_logout_user_can_access_user_posts(client, configed_app, post):
    with configed_app.test_request_context():
        id = str(post.getId())

        response = client.get("/user/test1", follow_redirects=False)

    assert response.status_code == 200
