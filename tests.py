import unittest

import flaskr
from models import User, Entry

flaskr.app.config.from_object('test_settings')

class FlaskrTestCase(unittest.TestCase):

    def setUp(self):
        self.session = flaskr.connect_with_sqlalchemy()
        self.app = flaskr.app.test_client()

    def tearDown(self):
        self.session.query(User).filter().delete()
        self.session.query(Entry).filter().delete()
        self.session.commit()

    def test_empty_db(self):
        resp = self.app.get('/')
        self.assertEqual(resp.status_code, 200)
        self.assertTrue("Unbelievable. No entries here so far" in resp.data)

    def test_register(self):
        resp = self.app.post("/register", data={'username': 'test', 'password': 'test'}, follow_redirects=True)
        self.assertEqual(resp.status_code, 200)
        self.assertTrue("You are registered" in resp.data)
        self.assertEqual(self.session.query(User).filter_by(username='test').count(), 1)

    def test_login(self):
        self.app.post("/register", data={'username': 'test', 'password': 'test'}, follow_redirects=True)
        resp = self.app.post("/login", data={'username': 'test', 'password': 'test'}, follow_redirects=True)
        self.assertEqual(resp.status_code, 200)
        self.assertTrue("You were logged in" in resp.data)

if __name__=='__main__':
    unittest.main()
