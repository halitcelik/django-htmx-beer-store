from django.conf import settings
from django.db import models
from django.shortcuts import reverse
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _


user = settings.AUTH_USER_MODEL

class Event(models.Model):
    name = models.CharField(_("Name"), max_length=50)
    date = models.DateField(_("Date"))
    hour = models.TimeField(_("Hour"))


    def __str__(self) -> str:
        return self.name

    def get_absolute_url(self):
        return reverse("events:detail", kwargs={"pk": self.pk})

    def get_delete_url(self):
        return reverse("events:delete", kwargs={"pk": self.pk})

class Attendee(models.Model):
    user = models.ForeignKey(user, verbose_name=_("User"), on_delete=models.CASCADE, blank=True, null=True)
    event = models.ForeignKey(Event, verbose_name=_("Event"), on_delete=models.CASCADE, related_name="attendees")
    first_name = models.CharField(_("First name"), max_length=50)
    last_name = models.CharField(_("Last name"), max_length=50)
    created = models.DateTimeField(_("Responded"), auto_now_add=True)
