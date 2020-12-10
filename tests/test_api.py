import unittest

from app.api.posts import edit_post
from app.models import Post, User
import json
import re
from base64 import b64encode
from app import create_app, db
from app.models import User, Role, Post, Comment


def test_true():
    assert True


def get_api_headers(username, password):
    return {
        "Authorization": "Basic "
        + b64encode((username + ":" + password).encode("utf-8")).decode("utf-8"),
        "Accept": "application/json",
        "Content-Type": "application/json",
    }


class EditPostTest(unittest.TestCase):
    def setup_method(self, method):
        self.app = create_app("testing")
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        Role.insert_roles()
        self.client = self.app.test_client()

    def teardown_method(self, method):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    # on teste le cas passant
    def test_author_can_edit_their_own_post(self):
        user = User(
            username="john@example.com",
            email="john@example.com",
            password="cat",
            confirmed=True,
        )
        db.session.add(user)
        db.session.flush()
        post = Post(author_id=user.id, body="toto")
        db.session.add(post)
        db.session.commit()

        url = f"/api/v1/posts/{post.id}"

        response = self.client.put(
            url,
            headers=get_api_headers("john@example.com", "cat"),
            data=json.dumps({"body": "updated body"}),
        )

        assert response.status_code == 200
        db.session.refresh(post)
        assert post.body == "updated body"

    # on teste le cas non-passant
    def test_user_cannot_edit_other_users_post(self):
        author = User(
            username="john@example.com",
            email="john@example.com",
            password="cat",
            confirmed=True,
        )
        bad_user = User(
            username="bad@example.com",
            email="bad@example.com",
            password="dog",
            confirmed=True,
        )
        db.session.add(author, bad_user)
        db.session.flush()

        post = Post(author_id=author.id, body="toto")
        db.session.add(post)
        db.session.commit()

        url = f"/api/v1/posts/{post.id}"

        response = self.client.put(
            url,
            headers=get_api_headers("bad@example.com", "dog"),
            data=json.dumps({"body": "updated body"}),
        )

        assert response.status_code == 403
        db.session.refresh(post)
        assert post.body == "toto"

    #  On teste le cas passant et le cas non passant
    def test_edit_post(self):
        author = User(
            username="john@example.com",
            email="john@example.com",
            password="cat",
            confirmed=True,
        )
        bad_user = User(
            username="bad@example.com",
            email="bad@example.com",
            password="dog",
            confirmed=True,
        )
        db.session.add(author, bad_user)
        db.session.flush()

        post = Post(author_id=author.id, body="toto")
        db.session.add(post)
        db.session.commit()

        url = f"/api/v1/posts/{post.id}"

        response = self.client.put(
            url,
            headers=get_api_headers("bad@example.com", "dog"),
            data=json.dumps({"body": "updated body"}),
        )

        assert response.status_code == 403
        db.session.refresh(post)
        assert post.body == "toto"

        response = self.client.put(
            url,
            headers=get_api_headers("john@example.com", "cat"),
            data=json.dumps({"body": "updated body"}),
        )
        assert response.status_code == 200
        db.session.refresh(post)
        assert post.body == "updated body"
