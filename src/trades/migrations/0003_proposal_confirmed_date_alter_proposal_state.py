# Generated by Django 5.0.3 on 2024-06-03 05:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("trades", "0002_rename_previous_proposal_proposal_counteroffer_to_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="proposal",
            name="confirmed_date",
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="proposal",
            name="state",
            field=models.CharField(
                choices=[
                    ("PENDING", "Pending"),
                    ("ACCEPTED", "Acepted"),
                    ("DECLINED", "Declined"),
                    ("COUNTEROFFERED", "Counteroffered"),
                    ("EXPIRED", "Expired"),
                    ("CANCELED", "Canceled"),
                ],
                default="PENDING",
                max_length=20,
            ),
        ),
    ]
