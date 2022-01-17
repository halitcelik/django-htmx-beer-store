from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.common.exceptions import WebDriverException
from django.urls import reverse
import time
from events.models import Event
from django.test import tag

MAX_WAIT = 10

class NewVisitorTest(StaticLiveServerTestCase):
    def setUp(self) -> None:
        self.browser = webdriver.Firefox()
        self.browser.get(self.live_server_url)
        return super().setUp()

    def tearDown(self) -> None:
        self.browser.quit()
        return super().tearDown()

    def test_home_page_can_be_seen(self):
        heading = self.browser.find_element(By.TAG_NAME, "h1").text
        self.wait_for_text_in_page("Django HTMX demo", heading)

    def test_create_page_can_be_seen(self):
        self.browser.get(self.get_full_url(reverse('events:create')))
        body = self.browser.find_element(By.TAG_NAME, "body").text
        self.wait_for_text_in_page("Please enter details about the event", body)

    def test_post_event_data_in_form(self):
        self.browser.get(self.get_full_url(reverse('events:create')))
        name_input = self.browser.find_element(By.NAME, "name")
        name_input.send_keys("Test event")
        date_input = self.browser.find_element(By.NAME, "date")
        date_input.click()
        date_input.send_keys(Keys.ARROW_DOWN, Keys.ARROW_LEFT, Keys.ENTER)
        hour_input = self.browser.find_element(By.NAME, "hour")
        hour_input.click()
        hour_input.send_keys("08", Keys.TAB, "20", Keys.TAB, "PM")
        self.browser.find_element(By.NAME, "submit").click()
        body = self.browser.find_element(By.TAG_NAME, "body").text
        self.wait_for_text_in_page("Test event", body)

    def test_post_attendee_data_in_form(self):
        event = Event.objects.create(name="Test event", date="2021-10-10", hour="20:20")
        self.browser.get(self.get_full_url(reverse('events:detail', kwargs={"pk": event.pk})))
        fname_input = self.browser.find_element(By.NAME, "first_name")
        fname_input.send_keys("Test Attendee First name")
        lname_input = self.browser.find_element(By.NAME, "last_name")
        lname_input.send_keys("Test Attendee Last name")
        self.browser.find_element(By.NAME, "submit").click()
        body = self.browser.find_element(By.TAG_NAME, "body").text
        self.wait_for_text_in_page("Test Attendee First name", body)
        self.wait_for_text_in_page(f"{event.attendees.count()} attending", body)
    
    
    def get_full_url(self, absolute_url):
        return f"{self.live_server_url}{absolute_url}"

    def wait_for_text_in_page(self, heading_text, container):
        start_time = time.time()
        while True:
            try:
                self.assertIn(heading_text, container)
                return
            except (AssertionError, WebDriverException) as e:
                if time.time() - start_time > MAX_WAIT:
                    raise e
                time.sleep(0.5)
    
    def wait_for_link_in_page(self, link_text):
        start_time = time.time()
        while True:
            try:
                element = self.browser.find_element(By.LINK_TEXT, link_text)
                element.click()
                return
            except (AssertionError, WebDriverException) as e:
                if time.time() - start_time > MAX_WAIT:
                    raise e
                time.sleep(0.5)

    