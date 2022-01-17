from django.test import TestCase
from django.test import tag
from django_htmx import middleware
from events.models import Event
from django.urls import reverse
from django_htmx.middleware import HtmxMiddleware
from django.http import HttpResponse


class HomePageTest(TestCase):
    def setUp(self) -> None:
        return super().setUp()
        
    def test_root_url_resolves_to_index_view(self):
        response = self.client.get("/", follow=True)
        self.assertTemplateUsed(response, "pages/home.html")

    def test_article_is_displayed(self):
        response = self.client.get(self.article.get_absolute_url())
        self.assertIn(self.article.title, response.content.decode())
        self.assertTemplateUsed(response, "blog/includes/article.html")
    
    def test_article_has_a_tag(self):
        self.assertIsNotNone(self.article.tags.first())

    @tag("last")
    def test_htmx_renders_partial(self):
        event = Event.objects.create(name="HTMX Test event", date="2021-10-10", hour="20:20")
        attendee_data = {
            "first_name": "Test Attendee First name",
            "last_name": "Test Attendee Last name",
        }
        response = self.client.post(
            reverse(
                'htmx_events:detail', 
                kwargs={"pk": event.pk}), 
                data=attendee_data, 
                follow=True, 
                HTTP_HX_REQUEST="true"
        )
        self.assertTemplateNotUsed(response, "htmx_events/event_detail.html")
        self.assertTemplateUsed(response, "htmx_events/includes/attendees-table.html")
    
    
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
