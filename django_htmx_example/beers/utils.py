from django.template import loader
from django.http import HttpResponse
import minify_html


def mini_render(
    request, template_name, context=None, content_type=None, status=None, using=None
):
    """
    Return an HttpResponse whose content is filled with the result of calling
    django.template.loader.render_to_string() with the passed arguments and minified using minify_html package.
    """
    content = minify_html.minify(
        loader.render_to_string(template_name, context, request, using=using)
    )
    return HttpResponse(content, content_type, status)
