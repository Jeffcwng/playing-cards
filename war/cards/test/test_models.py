from time import sleep

from django.core import mail
from django.core.exceptions import ValidationError
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.test import TestCase, LiveServerTestCase

from mock import patch, Mock
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.webdriver import WebDriver

from cards.forms import EmailUserCreationForm
from cards.models import Card, Player, WarGame
from cards.test.factories import WarGameFactory, PlayerFactory
from cards.test.utils import run_pyflakes_for_package, run_pep8_for_package
from cards.utils import create_deck, get_random_comic

class ModelTestCase(TestCase):
    def test_get_ranking(self):
        """Test that we get the proper ranking for a card"""
        card = Card.objects.create(suit=Card.CLUB, rank="jack")
        self.assertEqual(card.get_ranking(), 11)

        card = Card.objects.create(suit=Card.CLUB, rank="ace")
        self.assertEqual(card.get_ranking(), 14)

    def test_war_result(self):
        mycard = Card.objects.create(suit=Card.CLUB, rank="king")
        hiscard = Card.objects.create(suit=Card.CLUB, rank="jack")

        self.assertEqual(mycard.get_war_result(hiscard), 1)
        self.assertEqual(hiscard.get_war_result(mycard), -1)
        self.assertEqual(mycard.get_war_result(mycard), 0)

        myNEWcard = Card.objects.create(suit=Card.CLUB, rank="seven")
        hisNEWcard = Card.objects.create(suit=Card.HEART, rank="seven")
        self.assertEqual(hisNEWcard.get_war_result(myNEWcard), 0)


class ModelTestCase2(TestCase):
    def setUp(self):
        self.card = Card.objects.create(suit=Card.CLUB, rank="jack")

    def test_get_ranking(self):
        """Test that we get the proper ranking for a card"""
        self.assertEqual(self.card.get_ranking(), 11)


class PlayerModelTest(TestCase):
    def setUp(self):
        pass

    def create_war_game(self, user, result=WarGame.LOSS):
        WarGame.objects.create(result=result, player=user)

    def test_get_wins(self):
        user = PlayerFactory()
        # self.create_war_game(user, WarGame.WIN)
        # self.create_war_game(user, WarGame.WIN)
        # self.assertEqual(user.get_wins(), 2)
        WarGameFactory.create_batch(2, player=user, result=WarGame.WIN)
        self.assertEqual(user.get_wins(), 2)
        print "test get wins"

    def test_get_losses(self):
        print "test get losses"
        # user = Player.objects.create_user(username='test-user', email='test@test.com', password='password')
        # self.create_war_game(user, WarGame.LOSS)
        # self.create_war_game(user, WarGame.LOSS)
        # self.create_war_game(user, WarGame.LOSS)
        # self.assertEqual(user.get_losses(), 3)
        user = PlayerFactory()
        WarGameFactory.create_batch(3, player=user, result=WarGame.LOSS)
        self.assertEqual(user.get_losses(), 3)

    def test_get_ties(self):
        print "test get tie"
        user = PlayerFactory()
        WarGameFactory.create_batch(4, player=user, result=WarGame.TIE)
        self.assertEqual(user.get_ties(), 4)

    def test_get_record_display(self):
        user = PlayerFactory()
        WarGameFactory.create_batch(2, player=user, result=WarGame.WIN)
        WarGameFactory.create_batch(3, player=user, result=WarGame.LOSS)
        WarGameFactory.create_batch(4, player=user, result=WarGame.TIE)
        self.assertEqual(user.get_record_display(), "2-3-4")
        print "test display record"
