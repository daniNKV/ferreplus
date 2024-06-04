from django import forms
from django.utils import timezone
from datetime import datetime, date, timedelta, time
from .models import Proposal, DateSelection


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


class ConfirmDateForm(forms.Form):
    def __init__(self, proposal, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.proposal = proposal
        for i, date_selection in enumerate(proposal.possible_dates.all()):
            date_field = f"date_{i}"
            time_field = f"time_{i}"
            options_label = f'Puede desde {date_selection.from_time.strftime("%H:%M")} hasta {date_selection.to_time.strftime("%H:%M")}'
            formatted_date = date_selection.date.strftime("%A %d of %B %Y")
            self.fields[date_field] = forms.BooleanField(
                label=formatted_date,
                required=False,
                widget=forms.CheckboxInput(
                    attrs={"class": f"checkbox checkbox-{i} checkbox-md"}
                ),
            )
            self.fields[time_field] = forms.ChoiceField(
                label=options_label,
                choices=self.generate_datetime_choices(date_selection),
                required=False,
                widget=forms.Select(
                    attrs={
                        "class": f"select select-{i} select-md bg-dark text-neutral",
                        "style": "display: none;",
                    }
                ),
            )

    def clean(self):
        cleaned_data = super().clean()
        date_fields = [
            field
            for field in self.fields
            if field.startswith("date") and not field.startswith("actual_date")
        ]
        time_fields = [field for field in self.fields if field.startswith("time")]

        for i, (date_field, time_field) in enumerate(zip(date_fields, time_fields)):
            if cleaned_data.get(date_field):
                settled_time = cleaned_data[time_field]
                settled_date = self.proposal.possible_dates.all()[i].date

                # Assuming settled_time is a string in the format 'HH:MM'
                settled_hour, settled_minute = map(int, settled_time.split(":"))
                settled_datetime = datetime(
                    settled_date.year,
                    settled_date.month,
                    settled_date.day,
                    settled_hour,
                    settled_minute,
                )
                return settled_datetime

        raise forms.ValidationError("No date selected.")

    def generate_datetime_choices(self, date_selection):
        datetimes = []
        start_time = datetime.combine(date.today(), date_selection.from_time)
        end_time = datetime.combine(date.today(), date_selection.to_time)
        while start_time.time() <= end_time.time():
            datetime_str = start_time.time().strftime("%H:%M")
            datetimes.append((datetime_str, datetime_str))
            start_time += timedelta(minutes=15)
        return datetimes

    def field_pairs(self):
        fields = iter(self)
        return zip(fields, fields)
