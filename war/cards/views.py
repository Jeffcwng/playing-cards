# from django.conf import settings
from django.contrib.auth.decorators import login_required
# from django.core.mail import EmailMultiAlternatives
from django.shortcuts import render, redirect
from cards.forms import EmailUserCreationForm
from cards.models import Card, WarGame
from cards.utils import get_random_comic


def home(request):
    data = {
        'cards': Card.objects.all()
    }
    return render(request, 'cards.html', data)


def home_page(request):
    return render(request, 'home.html', {
        'comic': get_random_comic()
    })


def filters(request):
    data = {
        'cards': Card.objects.all()
    }

    return render(request, 'card_filters.html', data)


def template_tags(request):
    data = {
        'cards': Card.objects.all()
    }

    return render(request, 'card_template_tags.html', data)


def first_filter(request):
    data = {
        'cards': Card.objects.all()
    }

    return render(request, 'first_filter.html', data)


def suit_filter(request):
    data = {
        'cards': Card.objects.all()
    }

    return render(request, 'card_suits.html', data)


@login_required
def profile(request):
    # return render(request, 'profile.html', {
    #     'games': WarGame.objects.filter(player=request.user)
    # })
    return render(request, 'profile.html', {
        'games': WarGame.objects.filter(player=request.user),
        'wins': request.user.get_wins(),
        'losses': request.user.get_losses(),
        'ties': request.user.get_ties(),
        'record': request.user.get_record_display()

    })


def faq(request):
    return render(request, 'faq.html', {})


def blackjack(request):
    data = {
        'cards': Card.objects.order_by('?')[:2]
    }

    return render(request, 'blackjack.html', data)


def poker(request):
    data = {
        'cards': Card.objects.order_by('?')[:5]
    }

    return render(request, 'poker.html', data)


def register(request):
    if request.method == 'POST':
        form = EmailUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # text_content = 'Thank you for signing up for our website, {}'.format(user.username)
            # html_content = '<h2>Thanks {} for signing up!</h2> ' \
            #                '<div>I hope you enjoy using our site</div>'.format(user.username)
            # msg = EmailMultiAlternatives("Welcome!", text_content, settings.DEFAULT_FROM_EMAIL, [user.email])
            # msg.attach_alternative(html_content, "text/html")
            # msg.send()
            return redirect("profile")
    else:
        form = EmailUserCreationForm()

    return render(request, "registration/register.html", {
        'form': form,
    })


@login_required()
def war(request):
    cards = list(Card.objects.order_by('?'))
    user_card = cards[0]
    dealer_card = cards[1]

    result = user_card.get_war_result(dealer_card)
    WarGame.objects.create(result=result, player=request.user)

    return render(request, 'war.html', {
        'user_cards': [user_card],
        'dealer_cards': [dealer_card],
        'result': result})
