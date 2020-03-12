from accounts.models import Token
from django.test import TestCase
from unittest.mock import patch
import accounts.views


class SendLoginEmailViewTest(TestCase):
    """тест представления, которое отправляет
    ссобщение для входа в систему"""

    def test_redirects_to_home_page(self):
        """тест: переадресуется на домашнюю страницу"""
        response = self.client.post('/accounts/login?token=abcd123')
        self.assertRedirects(response, '/')

    @patch('accounts.views.send_mail')
    def test_send_mail_address_from_post(self, mock_send_mail):
        """тест: отправляет сообщение на адрес из метода post"""
        self.client.post('/accounts/send_login_email', data={
            'email':  'edith@example.com'
        })

        self.assertEqual(mock_send_mail.called, True)
        (subject, body, from_email, to_list), kwargs = mock_send_mail.call_args
        self.assertEqual(subject, 'Ваша ссылка для Суперблокнота')
        self.assertEqual(from_email, 'noreply@superlists')
        self.assertEqual(to_list, ['edith@example.com'])

    def test_adds_success_message(self):
        """тест: добавляется сообщение об успехе"""
        response = self.client.post('/accounts/send_login_email', data={
            'email': 'edith@example.com'
        }, follow=True)

        message = list(response.context['messages'])[0]
        self.assertEqual(
            message.message,
            "Проверьте свою почту, мы отправили Вам ссылку, которую можно использовать для входа на сайт."
        )
        self.assertEqual(message.tags, "success")

    def test_creates_token_associated_wih_email(self):
        """тест: создается маркер, связанный с элеткронной почтой"""
        self.client.post('/accounts/send_login_email', data={
            'email': 'edith@example.com'
        })
        token = Token.objects.first()
        self.assertEqual(token.email, 'edith@example.com')

    @patch('accounts.views.send_mail')
    def test_sends_link_to_login_using_token_uid(self, mock_send_mail):
        """тест: отсылается ссылка на вход в систему, используя uid маркера"""
        self.client.post('/accounts/send_login_email', data={
            'email': 'edith@example.com'
        })
        token = Token.objects.first()
        expected_url = f'http://testserver/accounts/login?token={token.uid}'
        (subject, body, from_email, to_list), kwargs = mock_send_mail.call_args
        self.assertIn(expected_url, body)
