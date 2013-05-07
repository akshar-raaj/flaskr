import unittest

from flask.ext.testing import TestCase

import main #To load the urls and views
import flaskr
from flaskr import app, db
from models import User, Entry

flaskr.app.config.from_object('test_settings')

class FlaskrTestCase(TestCase):

    def create_app(self):
        return app

    def setUp(self):
        pass

    def tearDown(self):
        User.query.delete()
        Entry.query.delete()
        db.session.commit()

    def test_empty_db(self):
        with self.app.test_client() as client:
            resp = client.get('/')
            self.assertEqual(resp.status_code, 200)
            self.assertTrue("Unbelievable. No entries here so far" in resp.data)

    def test_register(self):
        with self.app.test_client() as client:
            resp = client.post("/register", data={'username': 'test', 'password': 'test'}, follow_redirects=True)
            self.assertEqual(resp.status_code, 200)
            self.assertTrue("You are registered" in resp.data)
            self.assertEqual(User.query.filter_by(username='test').count(), 1)

    def test_login(self):
        with self.app.test_client() as client:
            client.post("/register", data={'username': 'test', 'password': 'test'}, follow_redirects=True)
            resp = client.post("/login", data={'username': 'test', 'password': 'test'}, follow_redirects=True)
            self.assertEqual(resp.status_code, 200)
            self.assertTrue("You were logged in" in resp.data)

if __name__=='__main__':
    unittest.main()
