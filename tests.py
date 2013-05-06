import unittest

import main #To load the urls and views
import flaskr
from flaskr import app, db
from models import User

flaskr.app.config.from_object('test_settings')

class FlaskrTestCase(unittest.TestCase):

    def setUp(self):
        c = app.config
        app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://%s:%s@%s/%s' % (c['DATABASE_USER'], c['DATABASE_PASSWORD'], 'localhost', c['DATABASE_NAME'])
        self.app = flaskr.app.test_client()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_empty_db(self):
        resp = self.app.get('/')
        self.assertEqual(resp.status_code, 200)
        self.assertTrue("Unbelievable. No entries here so far" in resp.data)

    def test_register(self):
        resp = self.app.post("/register", data={'username': 'test', 'password': 'test'}, follow_redirects=True)
        self.assertEqual(resp.status_code, 200)
        self.assertTrue("You are registered" in resp.data)
        self.assertEqual(User.query.filter_by(username='test').count(), 1)

    def test_login(self):
        self.app.post("/register", data={'username': 'test', 'password': 'test'}, follow_redirects=True)
        resp = self.app.post("/login", data={'username': 'test', 'password': 'test'}, follow_redirects=True)
        self.assertEqual(resp.status_code, 200)
        self.assertTrue("You were logged in" in resp.data)

if __name__=='__main__':
    unittest.main()
