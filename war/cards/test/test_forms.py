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
from cards.test.utils import run_pyflakes_for_package, run_pep8_for_package
from cards.utils import create_deck, get_random_comic

class FormTestCase(TestCase):
    def test_clean_username_exception(self):
        # Create a player so that this username we're testing is already taken
        Player.objects.create_user(username='test-user')

        # set up the form for testing
        form = EmailUserCreationForm()
        form.cleaned_data = {'username': 'test-user'}

        # use a context manager to watch for the validation error being raised
        with self.assertRaises(ValidationError):
            form.clean_username()

# class FormTestCase2(TestCase):
#     def test_clean_username_passes_exception(self):
#         Player.objects.create_user(username='new-user')
#         # set up the form for testing
#         form = EmailUserCreationForm()
#         form.cleaned_data = {'username': 'new-user'}
#
#         with self.assertRaises(ValidationError):
#             form.clean_username()
#         self.assertEqual(form.clean_username(), 'new-user')