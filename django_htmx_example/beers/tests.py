from django.test import TestCase
from django.test import tag
from django_htmx import middleware
from beers.models import Beer
from django.urls import reverse
from django_htmx.middleware import HtmxMiddleware
from django.http import HttpResponse


class HomePageTest(TestCase):
    def setUp(self) -> None:
        return super().setUp()

    def test_root_url_resolves_to_index_view(self):
        response = self.client.get("/", follow=True)
        self.assertTemplateUsed(response, "beers/click-to-edit.html")

    def test_htmx_renders_partial(self):
        beer = Beer.objects.create(name="test beer")
        response = self.client.post(
            reverse("beers:edit", kwargs={"pk": beer.pk}),
            follow=True,
            HTTP_HX_REQUEST="true",
        )
        self.assertTemplateNotUsed(response, "beers/edit.html")
        self.assertTemplateUsed(response, "beers/includes/form-row.html")

    def test_bool_default(self):
        request = self.request_factory.get("/")
        self.middleware(request)
        assert bool(request.htmx) is False

    def test_bool_false(self):
        request = self.request_factory.get("/", HTTP_HX_REQUEST="false")
        self.middleware(request)
        assert bool(request.htmx) is False

    def test_bool_true(self):
        request = self.request_factory.get("/", HTTP_HX_REQUEST="true")
        self.middleware(request)
        assert bool(request.htmx) is True
