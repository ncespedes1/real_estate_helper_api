from app import create_app
from app.models import Users, db
import unittest 
from werkzeug.security import check_password_hash, generate_password_hash
from app.util.auth import encode_token


# python -m unittest discover tests

class TestUsers(unittest.TestCase):


    def setUp(self): 
        self.app = create_app('TestingConfig')
        self.user = Users(first_name="Nik", last_name="Nak", email="tester@email.com",  password=generate_password_hash('abc123'))
        with self.app.app_context(): 
            db.drop_all()
            db.create_all()
            db.session.add(self.user)
            db.session.commit()
        self.token = encode_token(1, "free_user")
        self.client = self.app.test_client()


    def test_login(self):
        login_creds = {
            "email": "tester@email.com",
            "password": "abc123"
        }

        response = self.client.post('users/login', json=login_creds)
        self.assertTrue(response.status_code, 200)
        self.assertIn('token', response.json)

    def test_invalid_login(self):
        login_creds = {
            "email": "tester@email.com",
            "password": "not123"
        }

        response = self.client.post('/users', json=login_creds)
        self.assertEqual(response.status_code, 400)

    def test_create_user(self):
        user_payload = {
            "first_name": "New",
            "last_name": "Guy",
            "email": "newguy@email.com",
            "password": "abc123"
        }

        response = self.client.post('/users', json=user_payload)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json['first_name'], "New")
        self.assertTrue(check_password_hash(response.json['password'], "abc123"))


    def test_invalid_create(self):
        #missing email
        user_payload = {
            "first_name": "New",
            "last_name": "Guy",
            "password": "abc123"
        }

        response = self.client.post('/users', json=user_payload)
        self.assertEqual(response.status_code, 400)

    def test_nonunique_email(self):
        user_payload = {
            "first_name": "New",
            "last_name": "Guy",
            "email": "tester@email.com",
            "password": "abc123"
        }

        response = self.client.post('/users', json=user_payload)
        self.assertEqual(response.status_code, 400)