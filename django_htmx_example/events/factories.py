import pytz
import factory
from django.conf import settings
from factory.django import DjangoModelFactory


user = settings.AUTH_USER_MODEL

from django.utils.text import slugify

from events.models import Event, Attendee

class UserFactory(DjangoModelFactory):
    class Meta:
        model = user
    username = factory.Faker("first_name")
    name = factory.Faker("name")


    

def get_hour(obj):
    hour = f'{obj.date} {factory.Faker("time")}'
    return hour[:16]


class EventFactory(DjangoModelFactory):
    class Meta:
        model = Event

    name = factory.Faker("last_name")
    date = factory.Faker('date_time_this_year', tzinfo=pytz.utc)
    hour = factory.LazyAttribute(lambda obj: get_hour(obj))



class AttendeeFactory(DjangoModelFactory):
    class Meta:
        model = Attendee

    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    event = factory.SubFactory(EventFactory)
