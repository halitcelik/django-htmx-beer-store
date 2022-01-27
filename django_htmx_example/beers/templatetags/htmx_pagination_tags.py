from django import template
from django.conf import settings
from django.urls import reverse, NoReverseMatch
from django.utils.encoding import escape_uri_path
from django.template.loader import get_template

register = template.Library()


@register.simple_tag(takes_context=True)
def htmx_pagination(context, page, *args, **kwargs):
    request = context.get("request")
    query = request.GET.get("q")
    page_numbers = page.paginator.get_elided_page_range(
        page.number, on_each_side=2, on_ends=2
    )
    return get_template("pagination/pagination.html").render(
        {"page_numbers": page_numbers, "page_number": page.number, "query": query}
    )
