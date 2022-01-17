from django import forms  
from .models import Event, Attendee
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, ButtonHolder, Submit, Div
from django.urls import reverse


class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ["name", "date", "hour"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()

        self.helper.form_tag = False

        self.helper.layout = Layout(
            Div(
                Div(
                    Div(
                        "name",
                        css_class="form-group"
                    ),
                    css_class="col-md-10 col-md-offset-1"
                ),
                css_class="row"
            ),
            Div(
                Div(
                    Div(
                        "date",
                        css_class="form-group"
                    ),
                    css_class="col-md-5 col-md-offset-1"
                ),
                Div(
                    Div(
                        "hour",
                        css_class="form-group"
                    ),
                    css_class="col-md-5"
                ),
                css_class="row"
            )
        )
        Submit(
                "submit",
                "Submit",
                css_class="btn btn-info btn-fill btn-wd btn-next"
        )


    

class AttendeeForm(forms.ModelForm):
    class Meta:
        model = Attendee
        fields = ["first_name", "last_name"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()

        self.helper.form_tag = False

        self.helper.layout = Layout(
            Div(
                Div(
                    Div(
                        "first_name",
                        css_class="form-group"
                    ),
                    css_class="col-md-5 col-md-offset-1"
                ),
                Div(
                    Div(
                        "last_name",
                        css_class="form-group"
                    ),
                    css_class="col-md-5"
                ),
                css_class="row"
            )
        )
        Submit(
                "submit",
                "Submit",
                css_class="btn btn-info btn-fill btn-wd btn-next"
        )

