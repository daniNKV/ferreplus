from django import forms
from datetime import datetime, timedelta, time
from .models import DateSelection


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


class DatesSelectionForm(forms.ModelForm):
    class Meta:
        model = DateSelection
        fields = ["date", "from_time", "to_time"]

    from_time = forms.ChoiceField(
        choices=generate_time_choices,
        required=False,
        widget=forms.widgets.Select(
            attrs={
                "class": "select select-bordered bg-neutral text-dark font-semibold border-2 border-dark w-full"
            },
        ),
    )
    to_time = forms.ChoiceField(
        choices=generate_time_choices,
        required=False,
        widget=forms.widgets.Select(
            attrs={
                "class": "select select-bordered bg-neutral text-dark font-semibold border-2 border-dark w-full"
            }
        ),
    )
    date = forms.ChoiceField(
        choices=generate_date_choices(),
        required=False,
        widget=forms.widgets.Select(
            attrs={
                "class": "select select-bordered bg-neutral text-dark font-semibold border-2 border-dark w-full"
            }
        ),
    )

    def clean(self):
        cleaned_data = super().clean()
        date_str = cleaned_data.get("date")
        if date_str:
            cleaned_data["date"] = datetime.strptime(date_str, "%Y-%m-%d").date()
        for field in ["from_time", "to_time"]:
            time_str = cleaned_data.get(field)
            if time_str:
                hour, minute, second = map(int, time_str.split(":"))
                cleaned_data[field] = time(hour, minute)
        return cleaned_data
