from django.test import TestCase
from django.contrib.auth import get_user_model
from accounts.models import User, Token

User = get_user_model()


class UserModelTest(TestCase):

    def test_list_user_is_valid_with_email_only(self):
        user = User(email='ab@ab.com')
        user.full_clean


class TokenModelTest(TestCase):

    def test_links_user_with_auto_generated_uid(self):
        token1 = Token.objects.create(email='hello@hello.com')
        token2 = Token.objects.create(email='hello@hello.com')
        self.assertNotEqual(token1.uid, token2.uid)
