from fixtures import user, client, configed_app, login, post


def test_logged_user_can_access_account(user, client, configed_app, login):
    with configed_app.test_request_context():
        response = client.get("/account", follow_redirects=False)

    assert response.status_code == 200, (
        f"Logged user does not have access account. Status code: {response.status_code}"
    )


def test_logged_user_can_access_logout(user, client, configed_app, login):
    with configed_app.test_request_context():
        response = client.get("/logout", follow_redirects=False)

    assert response.status_code == 302, (
        f"Logged user does not have access logout. Status code: {response.status_code}"
    )


def test_logged_user_can_access_post_delete(user, client, configed_app, login, post):
    with configed_app.test_request_context():
        id = str(post.getId())
        response = client.get("/post/" + id + "/delete", follow_redirects=False)

    assert response.status_code == 302, (
        f"Logged user does not have access delete. Status code: {response.status_code}"
    )


def test_logged_user_can_access_post_update(user, client, configed_app, login, post):
    with configed_app.test_request_context():
        id = str(post.getId())
        response = client.get("/post/" + id + "/update", follow_redirects=False)

    assert response.status_code == 200, (
        f"Logged user does not have access update. Status code: {response.status_code}"
    )


def test_logged_user_can_access_post_new(client, configed_app, login):
    with configed_app.test_request_context():
        response = client.get("/post/new", follow_redirects=False)

    assert response.status_code == 200, (
        f"Logged user does not have access create new post. Status code: {response.status_code}"
    )


def test_logged_user_can_access_home_page(client, configed_app, login):
    with configed_app.test_request_context():
        response = client.get("/home", follow_redirects=False)

    assert response.status_code == 200, (
        f"Logged user does not have access home page. Status code: {response.status_code}"
    )


def test_logged_user_can_access_post_id(user, client, configed_app, login, post):
    with configed_app.test_request_context():
        id = str(post.getId())
        response = client.get("/post/" + id, follow_redirects=False)

    assert response.status_code == 200, (
        f"Logged user does not have access post id. Status code: {response.status_code}"
    )


def test_logged_user_can_access_user_posts(client, configed_app, login):
    with configed_app.test_request_context():
        response = client.get("/user/test1", follow_redirects=False)

    assert response.status_code == 200, (
        f"Logged user does not have access user's posts. Status code: {response.status_code}"
    )
