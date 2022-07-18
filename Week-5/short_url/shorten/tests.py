from django.test import TestCase,Client
from mongoengine import *



class TestForAccounts(TestCase):
    # def setup_databases(self, **kwargs):
    #     pass
    #
    # def teardown_databases(self, old_config, **kwargs):
    #     pass

    def _fixture_setup(self):
        pass

    def _fixture_teardown(self):
        pass

    def test_login(self):
        c = Client()
        response = c.post('/account/login', {'name': 'abcd', 'password': '1234'})
        self.assertEqual(response.status_code,200)
