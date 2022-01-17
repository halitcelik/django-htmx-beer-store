from django.shortcuts import get_object_or_404, render
from django.db.models import Count
from events.models import Event, Attendee
from events.forms import EventForm, AttendeeForm
from django.http import HttpResponseRedirect
from django.urls import reverse

def all_events(request):
    events = Event.objects.all()
    return render(request, "htmx_events/list.html", {"events": events})


def detail(request, pk):
    event = Event.objects.filter(pk=pk).prefetch_related("attendees").annotate(attendees_count=Count("attendees")).first()
    form = AttendeeForm()
    template = "htmx_events/event_detail.html"
    if request.method == "POST":
        form = AttendeeForm(request.POST)
        if form.is_valid():
            attendee = form.save(commit=False)
            attendee.event = event
            attendee.save()
            if request.htmx:
                template = "htmx_events/includes/attendees-table.html"
                return render(request, template, {"event": event, "form": form})
            return HttpResponseRedirect(reverse("htmx_events:detail", kwargs={'pk': event.pk}))
    return render(request, template, {"event": event, "form": form})


def delete(request, pk):
    event = get_object_or_404(Event, pk=pk)
    if request.method == "POST":
        if event and request.user == event.user:
            event.delete()
            return HttpResponseRedirect(reverse("events:all"))

def create(request):
    form = EventForm()
    if request.method == "POST":
        form = EventForm(request.POST)
        if form.is_valid():
            event = form.save()
            return HttpResponseRedirect(reverse("htmx_events:detail", kwargs={'pk': event.pk}))
    return render(request, "htmx_events/create.html", {"form": form})


def organising(request):
    events = Event.objects.none
    if request.user.is_authenticated:
        events = Event.objects.filter(user=request.user)
    return render(request, "events/organising.html", {"events": events})