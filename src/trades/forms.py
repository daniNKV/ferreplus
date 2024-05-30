from django import forms
from datetime import datetime, timedelta, time
from .models import Appointment


def generate_time_choices():
    times = [
        (time(hour, minute), f"{hour}:{minute:02}")
        for hour in range(9, 19)
        for minute in range(0, 60, 15)
    ]
    return times


def generate_date_choices():
    dates = [
        (
            (datetime.now() + timedelta(days=i)).date(),
            (datetime.now() + timedelta(days=i)).strftime("%A %d"),
        )
        for i in range(1, 15)
        if (datetime.now() + timedelta(days=i)).weekday() < 6
    ]
    return dates


class DatesForm(forms.Form):
    class Meta:
        model: Appointment
    date1 = forms.ChoiceField(
        required=True,
        label="Dia 1",
        choices=[],
        widget=forms.widgets.Select(
            attrs={"class": "select select-bordered bg-neutral text-dark font-semibold border-2 border-dark w-full"}
        ),
    )
    time1 = forms.ChoiceField(
        required=True,
        label="Horario 1",
        choices=[],
        widget=forms.widgets.Select(
            attrs={"class": "select select-bordered bg-neutral text-dark font-semibold border-2 border-dark w-full"}
        ),
    )
    date2 = forms.ChoiceField(
        required=True,
        label="Dia 2",
        choices=[],
        widget=forms.widgets.Select(
            attrs={"class": "select select-bordered bg-neutral text-dark font-semibold border-2 border-dark w-full"}
        ),
    )
    time2 = forms.ChoiceField(
        required=True,
        label="Horario 2",
        choices=[],
        widget=forms.widgets.Select(
            attrs={"class": "select select-bordered bg-neutral text-dark font-semibold border-2 border-dark w-full"}
        ),
    )
    date3 = forms.ChoiceField(
        label="Dia 3",
        choices=[],
        widget=forms.widgets.Select(
            attrs={"class": "select select-bordered bg-neutral text-dark font-semibold border-2 border-dark w-full"}
        ),
    )
    time3 = forms.ChoiceField(
        label="Horario 3",
        choices=[],
        widget=forms.widgets.Select(
            attrs={"class": "select select-bordered bg-neutral text-dark font-semibold border-2 border-dark w-full"}
        ),
    )

    def __init__(self, *args, **kwargs):
        super(DatesForm, self).__init__(*args, **kwargs)
        time_choices = generate_time_choices()
        date_choices = generate_date_choices()
        self.fields["date1"].choices = date_choices
        self.fields["time1"].choices = time_choices
        self.fields["date2"].choices = date_choices
        self.fields["time2"].choices = time_choices
        self.fields["date3"].choices = date_choices
        self.fields["time3"].choices = time_choices
        self.date_tuple1 = None
        self.date_tuple2 = None
        self.date_tuple3 = None


    def clean(self):
        cleaned_data = super().clean()
        date1 = cleaned_data.get('date1')
        time1 = cleaned_data.get('time1') 
        date2 = cleaned_data.get('date2')
        time2 = cleaned_data.get('time2')
        date3 = cleaned_data.get('date3')
        time3 = cleaned_data.get('time3')
 
        # if date1 == date2 and time1 == time2:
        #     raise forms.ValidationError("Las selecciones de fecha/hora primera y segunda no pueden ser iguales.")

        # if date1 == date3 and time1 == time3:
        #     raise forms.ValidationError("Las selecciones de fecha/hora primera y tercera no pueden ser iguales.")

        # if date2 == date3 and time2 == time3:
        #     raise forms.ValidationError("Las selecciones de fecha/hora segunda y tercera no pueden ser iguales.")

        return cleaned_data