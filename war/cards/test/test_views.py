from time import sleep

from django.core import mail
from django.core.exceptions import ValidationError
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.test import TestCase, LiveServerTestCase
from selenium.webdriver.firefox.webdriver import WebDriver
from mock import patch, Mock
from selenium.webdriver.common.keys import Keys

from cards.forms import EmailUserCreationForm
from cards.models import Card, Player, WarGame
from cards.test.factories import PlayerFactory
from cards.test.utils import run_pyflakes_for_package, run_pep8_for_package
from cards.utils import create_deck, get_random_comic


class ViewTestCase(TestCase):
    def create_war_game(self, user, result=WarGame.LOSS):
        WarGame.objects.create(result=result, player=user)

    def setUp(self):
        create_deck()

    def test_home_page(self):
        response = self.client.get(reverse('home'))
        self.assertIn(b'<p>Suit: spade, Rank: two</p>', response.content)
        self.assertEqual(response.context['cards'].count(), 52)

    def test_faq_page(self):
        response = self.client.get(reverse('faq'))
        self.assertIn(b'<p>Q: Can I win real money on this website?</p>', response.content)
        # self.assertEqual(response.context['cards'].count(), 52)

    def test_filters_page(self):
        response = self.client.get(reverse('filters'))
        self.assertIn(b'Capitalized Suit: 0', response.content)
        self.assertEqual(response.context['cards'].count(), 52)

    def test_register_page(self):
        username = 'new-user'
        data = {
            'username': username,
            'email': 'test@test.com',
            'password1': 'test',
            'password2': 'test'
        }
        response = self.client.post(reverse('register'), data)

        # Check this user was created in the database
        self.assertTrue(Player.objects.filter(username=username).exists())

        # Check it's a redirect to the profile page
        self.assertIsInstance(response, HttpResponseRedirect)
        self.assertTrue(response.get('location').endswith(reverse('profile')))

    def test_login_page(self):
        username = 'new-user'
        data = {
            'username': username,
            'email': 'test@test.com',
            'password1': 'test',
            'password2': 'test'
        }
        # response = self.client.post(reverse('login'), data)
        # self.assertIsInstance(response, HttpResponseRedirect)
        # self.assertTrue(response.get('location').endswith(reverse('profile')))


    def test_profile_page(self):
        # Create user and log them in
        password = 'passsword'
        # user = Player.objects.create_user(username='test-user', email='test@test.com', password=password)
        user = PlayerFactory()
        self.client.login(username=user.username, password=password)

        # Set up some war game entries
        self.create_war_game(user)
        self.create_war_game(user, WarGame.WIN)
        self.create_war_game(user, WarGame.LOSS)
        self.create_war_game(user, WarGame.TIES)

        # Make the url call and check the html and games queryset length
        response = self.client.get(reverse('profile'))
        self.assertInHTML('<p>Your email address is {}</p>'.format(user.email), response.content)
        self.assertEqual(len(response.context['games']), 2)


    def test_war_page(self):
        response = self.client.get(reverse('war'))
        self.assertInHTML("War!", response.content)
        # self.assertEqual(response.context['cards'].count(), 52)


    @patch('cards.utils.requests')
    def test_home_page(self, mock_requests):
        pass

    @patch('cards.utils.requests')
    def test_xkcd(self, mock_requests):
        mock_requests.return_value = 5
        self.assertEqual(mock_requests.return_value, 5)

    @patch('cards.utils.requests')
    def test_xkcd2(self, mock_requests):
        print("this test is running")
        mock_comic = {
        'num': 1433,
        'year': "2014",
        'safe_title': "Lightsaber",
        'alt': "A long time in the future, in a galaxy far, far, away.",
        'transcript': "An unusual gamma-ray burst originating from somewhere across the universe.",
        'img': "http://imgs.xkcd.com/comics/lightsaber.png",
        'title': "Lightsaber",
    }
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = mock_comic
        mock_requests.get.return_value = mock_response
        self.assertEqual(get_random_comic()['num'],1433)
        response = self.client.get(reverse('home_page'))
        self.assertInHTML('<h3>{} - {}</h3>'.format(mock_comic['safe_title'], mock_comic['year']), response.content)
        self.assertInHTML('<img alt="{}" src="{}">'.format(mock_comic['alt'], mock_comic['img']), response.content)
        self.assertInHTML('<p>{}</p>'.format(mock_comic['transcript']), response.content)

