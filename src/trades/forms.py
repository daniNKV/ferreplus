from django import forms
from datetime import datetime, timedelta


def generate_time_choices():
    times = [
        (datetime(2000, 1, 1, hour, minute), f"{hour}:{minute:02}")
        for hour in range(9, 19)
        for minute in range(0, 60, 15)
    ]
    return times


def generate_date_choices():
    dates = [
        (
            datetime.now() + timedelta(days=i),
            (datetime.now() + timedelta(days=i)).strftime("%Y-%m-%d"),
        )
        for i in range(1, 15)
        if (datetime.now() + timedelta(days=i)).weekday() < 5
    ]
    return dates


class TradeForm(forms.Form):
    date1 = forms.ChoiceField(
        required=True,
        label="Dia 1",
        choices=[],
        widget=forms.widgets.Select(
            attrs={"class": "select select-bordered bg-dark text-neutral w-full"}
        ),
    )
    time1 = forms.ChoiceField(
        required=True,
        label="Horario 1",
        choices=[],
        widget=forms.widgets.Select(
            attrs={"class": "select select-bordered bg-dark text-neutral w-full"}
        ),
    )
    date2 = forms.ChoiceField(
        required=True,
        label="Dia 2",
        choices=[],
        widget=forms.widgets.Select(
            attrs={"class": "select select-bordered bg-dark text-neutral w-full"}
        ),
    )
    time2 = forms.ChoiceField(
        required=True,
        label="Horario 2",
        choices=[],
        widget=forms.widgets.Select(
            attrs={"class": "select select-bordered bg-dark text-neutral w-full"}
        ),
    )
    date3 = forms.ChoiceField(
        label="Dia 3",
        choices=[],
        widget=forms.widgets.Select(
            attrs={"class": "select select-bordered bg-dark text-neutral w-full"}
        ),
    )
    time3 = forms.ChoiceField(
        label="Horario 3",
        choices=[],
        widget=forms.widgets.Select(
            attrs={"class": "select select-bordered bg-dark text-neutral w-full"}
        ),
    )

    def __init__(self, *args, **kwargs):
        super(TradeForm, self).__init__(*args, **kwargs)
        self.fields["date1"].choices = generate_date_choices()
        self.fields["time1"].choices = generate_time_choices()
        self.fields["date2"].choices = generate_date_choices()
        self.fields["time2"].choices = generate_time_choices()
        self.fields["date3"].choices = generate_date_choices()
        self.fields["time3"].choices = generate_time_choices()
