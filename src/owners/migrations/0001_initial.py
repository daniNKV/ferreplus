# Generated by Django 5.0.3 on 2024-05-07 13:03

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Branch',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('address', models.CharField(max_length=100)),
                ('opening_hour', models.TimeField()),
                ('closing_hour', models.TimeField()),
            ],
        ),
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=100)),
                ('birth_date', models.DateField()),
                ('last_name', models.CharField(max_length=100)),
                ('dni', models.CharField(max_length=8)),
                ('branch_id', models.CharField(max_length=100)),
            ],
        ),
    ]
