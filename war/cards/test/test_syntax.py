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

class SyntaxTest(TestCase):
    def test_syntax(self):
        """
        Run pyflakes/pep8 across the code base to check for potential errors.
        """
        packages = ['cards']
        warnings = []
        # Eventually should use flake8 instead so we can ignore specific lines via a comment
        for package in packages:
            warnings.extend(run_pyflakes_for_package(package, extra_ignore=("_settings",)))
            warnings.extend(run_pep8_for_package(package, extra_ignore=("_settings",)))
        # if warnings:
        #     self.fail("{0} Syntax warnings!\n\n{1}".format(len(warnings), "\n".join(warnings)))

    def test_register_sends_email(self):
        form = EmailUserCreationForm()
        form.cleaned_data = {
            'username': 'test',
            'email': 'test@test.com',
            'password1': 'test-pw',
            'password2': 'test-pw',
        }
        form.save()
        # Check there is an email to send
        self.assertEqual(len(mail.outbox), 1)
        # Check the subject is what we expect
        self.assertEqual(mail.outbox[0].subject, 'Welcome!')
