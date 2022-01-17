from django import template
from django.conf import settings
from django.urls import reverse, NoReverseMatch
from django.utils.encoding import escape_uri_path
from django.template.loader import get_template
register = template.Library()


@register.simple_tag(takes_context=True)
def is_in_favourites(context, beer, *args, **kwargs):
    request = context.get('request')
    if request is None or not request.user.is_authenticated:
        # Can't work without the request object.
        return ''

    if request.user.favourites.filter(pk=beer.pk).exists():
        return "btn-danger"
    else:
        return ""


@register.simple_tag(takes_context=True)
def favourites_count(context, *args, **kwargs):
    request = context.get('request')
    if request is None or not request.user.is_authenticated:
        return ""
    else:
       return get_template("beers/includes/favourites-count.html").render(
            {"count": request.user.favourites.count()}
        )