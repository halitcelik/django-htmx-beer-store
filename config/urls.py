from django.conf import settings
from django.conf.urls.i18n import i18n_patterns
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.views import defaults as default_views
from django.views.generic import TemplateView
from django.views.generic.base import RedirectView

urlpatterns = i18n_patterns(
    path("", RedirectView.as_view(permanent=False, url="examples/click-to-edit")),
    path(
        "about/", TemplateView.as_view(template_name="pages/about.html"), name="about"
    ),
    # Django Admin, use {% url 'admin:index' %}
    path(settings.ADMIN_URL, admin.site.urls),
    # User management
    path("users/", include("django_htmx_example.users.urls", namespace="users")),
    path("examples/", include("beers.urls", namespace="examples")),
    path("accounts/", include("allauth.urls")),
    # Your stuff: custom urls includes go here
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += [
    path("i18n/", include("django.conf.urls.i18n")),
    path("group-items/", include("admin_group_items.urls")),
]

if settings.DEBUG:
    # This allows the error pages to be debugged during development, just visit
    # these url in browser to see how these error pages look like.
    urlpatterns += [
        path(
            "400/",
            default_views.bad_request,
            kwargs={"exception": Exception("Bad Request!")},
        ),
        path(
            "403/",
            default_views.permission_denied,
            kwargs={"exception": Exception("Permission Denied")},
        ),
        path(
            "404/",
            default_views.page_not_found,
            kwargs={"exception": Exception("Page not Found")},
        ),
        path("500/", default_views.server_error),
    ]
    if "debug_toolbar" in settings.INSTALLED_APPS:
        import debug_toolbar

        urlpatterns = [path("__debug__/", include(debug_toolbar.urls))] + urlpatterns
