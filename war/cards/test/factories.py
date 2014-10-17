import factory
from cards.models import Player, WarGame, Card


class WarGameFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'cards.WarGame'
    # result = WarGame.TIE


class PlayerFactory(factory.DjangoModelFactory):
    class Meta:
        model = Player
    # username = factory.Sequence(lambda i: 'User%d' % i)
    # email = factory.lazy_attribute(lambda o: '%s@gmail.com' % o.username)
    # or
    # profile = factory.SubFactory(ProfileFactory)
        #django_get_or_create = ('username', 'email', 'password')

    username = 'tom'
    email = 'tom@tom.com'
    password = 'password'


