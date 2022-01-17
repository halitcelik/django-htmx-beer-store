from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.views import defaults as default_views
from django.views.generic import TemplateView
from .views import all_events, detail, delete, organising, create


app_name = "events"

urlpatterns = [
    path("all", all_events, name="all"),
    path("<int:pk>", detail, name="detail"),
    path("delete/<int:pk>", delete, name="delete"),
    path("create", create, name="create"),
    path("organising", organising, name="organising")
]
