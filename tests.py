import unittest

from server import app
from model import db, connect_to_db
from sample_data import example_data
import get_twitter_posts
from generate_hex import match_foundation_shade
from get_twitter_posts import load_tweets


class RegistrationTests(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()
        app.config["TESTING"] = True
        connect_to_db(app, "postgresql:///testdb")
        db.create_all()
        example_data()

    def tearDown(self):
        db.session.close()
        db.drop_all()

    def test_display_form(self):
        result = self.client.get("/registration")
        self.assertIn(b"password", result.data)

    def test_redirect(self):
        result = self.client.post("/registration", data={"first_name": "Bobby", "last_name": "Bob", "email": "bobbers@gmail.com", "password": "1234",
                                  "birthday_month": "January", "birthday_day": 12, "birthday_year": 1991}, follow_redirects=True)
        self.assertIn(b"Email address", result.data)

    def test_user_add(self):
        result = self.client.post("/login", data={"user_email": "bobbybob@gmail.com", "user_password": "1234"},
                                  follow_redirects=True)
        self.assertIn(b"Bobby", result.data)


class LoginTests(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()
        app.config["TESTING"] = True
        connect_to_db(app, "postgresql:///testdb")
        db.create_all()
        example_data()

    def tearDown(self):
        db.session.close()
        db.drop_all()

    def test_display_form(self):
        result = self.client.get("/login")
        self.assertIn(b"Email address", result.data)

    def test_redirect(self):
        result = self.client.post("/login", data={"user_email": "bobbybob@gmail.com", "user_password": "1234"},
                                  follow_redirects=True)
        self.assertIn(b"I'd like to Select an Image to View Matches", result.data)

    def test_redirect_no_registration(self):
        result = self.client.post("/login", data={"user_email": "charlie@charles.com", "user_password": "1234"},
                                  follow_redirects=True)
        self.assertIn(b"First Name", result.data)


class SelectImageTests(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()
        app.config["TESTING"] = True
        app.config["SECRET_KEY"] = "ABC"
        connect_to_db(app, "postgresql:///testdb")
        db.create_all()
        example_data()

        with self.client as c:
            with c.session_transaction() as sess:
                sess["user_id"] = 1

    def tearDown(self):
        db.session.close()
        db.drop_all()

    def test_image_display(self):
        result = self.client.get("/select_image")

        self.assertIn(b"/static/uploads/girl-glowing-skin-blue-eyes.jpg", result.data)


class SelectImageTestsNoLogin(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()
        app.config["TESTING"] = True
        app.config["SECRET_KEY"] = "ABC"
        connect_to_db(app, "postgresql:///testdb")
        db.create_all()
        example_data()

    def tearDown(self):
        db.session.close()
        db.drop_all()

    def test_image_no_login(self):
        result = self.client.get("/select_image", follow_redirects=True)

        self.assertIn(b"Password", result.data)


class FavoritesTests(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()
        app.config["TESTING"] = True
        app.config["SECRET_KEY"] = "ABC"
        connect_to_db(app, "postgresql:///testdb")
        db.create_all()
        example_data()

        with self.client as c:
            with c.session_transaction() as sess:
                sess["user_id"] = 1

    def tearDown(self):
        db.session.close()
        db.drop_all()

    def test_display_favorite(self):
        result = self.client.get("/view_favorites")
        self.assertIn(b"s1925148", result.data)

    def test_popovers(self):
        result = self.client.get("/view_favorites")
        self.assertIn(b"popover", result.data)


class TestFavoritesNoLogin(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()
        app.config["TESTING"] = True
        app.config["SECRET_KEY"] = "ABC"
        connect_to_db(app, "postgresql:///testdb")
        db.create_all()
        example_data()

    def tearDown(self):
        db.session.close()
        db.drop_all()

    def fav_no_login(self):
        result = self.client.get("/view_favorites", follow_redirects=True)
        self.assertIn(b"Password", result.data)

class TestSubmitImage(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()
        app.config["TESTING"] = True
        app.config["SECRET_KEY"] = "ABC"
        connect_to_db(app, "postgresql:///testdb")
        db.create_all()
        example_data()

        with self.client as c:
            with c.session_transaction() as sess:
                sess["user_id"] = 1

    def tearDown(self):
        db.session.close()
        db.drop_all()

    def display_form(self):
        result = self.client.get("/submit_image")
        self.assertIn(b"multipart/form-data", result.data)


class TestSubmitImageNoLogin(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()
        app.config["TESTING"] = True
        app.config["SECRET_KEY"] = "ABC"
        connect_to_db(app, "postgresql:///testdb")
        db.create_all()
        example_data()

    def tearDown(self):
        db.session.close()
        db.drop_all()

    def submit_image_no_login(self):
        result = self.client.get("/submit_image", follow_redirects=True)
        self.assertIn(b"Password", result.data)


class TestReviews(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()
        app.config["TESTING"] = True
        app.config["SECRET_KEY"] = "ABC"
        connect_to_db(app, "postgresql:///testdb")
        db.create_all()
        example_data()

        with self.client as c:
            with c.session_transaction() as sess:
                sess["user_id"] = 1

    def tearDown(self):
        db.session.close()
        db.drop_all()

    def test_display_review(self):
        result = self.client.get("/brand/P87985432")
        self.assertIn(b"ever ever", result.data)

    def test_review_form(self):
        result = self.client.get("/brand/P87985432")
        self.assertIn(b"review_form", result.data)


class TestMatches(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()
        app.config["TESTING"] = True
        app.config["SECRET_KEY"] = "ABC"
        connect_to_db(app, "postgresql:///testdb")
        db.create_all()
        example_data()

        with self.client as c:
            with c.session_transaction() as sess:
                sess["user_id"] = 1

    def tearDown(self):
        db.session.close()
        db.drop_all()


    def test_match_display(self):
        result = self.client.get("/display_matches/1")
        self.assertIn(b"s1925155", result.data)

    def test_popover(self):
        result = self.client.get("/display_matches/1")
        self.assertIn(b"popover", result.data)


class TestYouMayAlsoLike(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()
        app.config["TESTING"] = True
        app.config["SECRET_KEY"] = "ABC"
        connect_to_db(app, "postgresql:///testdb")
        db.create_all()
        example_data()

        with self.client as c:
            with c.session_transaction() as sess:
                sess["user_id"] = 1

        def _mock_match_foundation_shade(fav_hex, foundation_hex_lst):
            return ["#EECDB1","#F4D6B9","#EFD1B3","#E8D2BB","#F2CCB2","#EDC8B4"]
        generate_hex.match_foundation_shade = _mock_match_foundation_shade

        closest_matches = Foundation.query.filter(Foundation.foundation_hex_code.in_(top_hex_matches)).all()

    def tearDown(self):
        db.session.close()
        db.drop_all()

    def displayAlsoLike(self):
        result = self.client.get("/view_favorites")
        self.assertIn(b"11925205", result.data)


class TestTwitterCarouselNoHandle(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()
        app.config["TESTING"] = True
        app.config["SECRET_KEY"] = "ABC"
        connect_to_db(app, "postgresql:///testdb")
        db.create_all()
        example_data()

        with self.client as c:
            with c.session_transaction() as sess:
                sess["user_id"] = 1

        def _mock_load_tweets_no_twitter(brand):
            return []
        load_tweets = _mock_load_tweets_no_twitter

    def tearDown(self):
        db.session.close()
        db.drop_all()

    def test_no_carousel(self):
        result = self.client.get("/brand/P400888")
        self.assertIn(b"No Brand Images", result.data)


class TestTwitterCarouselNoPosts(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()
        app.config["TESTING"] = True
        app.config["SECRET_KEY"] = "ABC"
        connect_to_db(app, "postgresql:///testdb")
        db.create_all()
        example_data()

        with self.client as c:
            with c.session_transaction() as sess:
                sess["user_id"] = 1

        def _mock_load_tweets_no_posts(brand):
            return []
        load_tweets = _mock_load_tweets_no_posts

    def tearDown(self):
        db.session.close()
        db.drop_all()

    def test_no_carousel(self):
        result = self.client.get("/brand/P432234")
        self.assertIn(b"No Brand Images", result.data)


class TestTwitterCarouseNoMedia(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()
        app.config["TESTING"] = True
        app.config["SECRET_KEY"] = "ABC"
        connect_to_db(app, "postgresql:///testdb")
        db.create_all()
        example_data()

        with self.client as c:
            with c.session_transaction() as sess:
                sess["user_id"] = 1

        def _mock_load_tweets_no_media(brand):
            return []
        load_tweets = _mock_load_tweets_no_media

    def tearDown(self):
        db.session.close()
        db.drop_all()


    def test_no_Ccarousel(self):
        result = self.client.get("/brand/P427301")
        self.assertIn(b"No Brand Images", result.data)



if __name__ == "__main__":
    unittest.main()
