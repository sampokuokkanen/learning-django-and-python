from django.test import TestCase
from accounts.models import Token, User
from accounts.authentication import PasswordlessAuthenticationBackend


class SendEmailTest(TestCase):

    def test_test_adds_success_message(self):
        response = self.client.post('/accounts/send_login_email', data={
            'email': 'edith@example.com'
        }, follow=True)

        message = list(response.context['messages'])[0]
        self.assertEqual(
            message.message,
            "Check your email, we've sent you a link you can use to log in"
        )
        self.assertEqual(message.tags, 'success')

class LoginViewTest(TestCase):

    def test_redirects_to_home_page(self):
        response = self.client.get('/accounts/login?token=abc123')
        self.assertRedirects(response, '/')

    def test_creates_token_associated_with_email(self):
        self.client.post('/accounts/send_login_email', data={
            'email': 'edith@example.com'
        })
        token = Token.objects.first()
        self.assertEqual(token.email, 'edith@example.com')

    def test_returns_existing_user_with_correct_email_if_token_exists(self):
        email = 'edith@example.com'
        existing_user = User.objects.create(email=email)
        request = self.client.post('/accounts/send_login_email', data={
            'email': email
        })
        token = Token.objects.first()
        user = PasswordlessAuthenticationBackend().authenticate(request, token.uid)
        self.assertEqual(user, existing_user)