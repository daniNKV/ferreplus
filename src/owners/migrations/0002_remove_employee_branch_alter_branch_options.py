# Generated by Django 5.0.6 on 2024-05-12 13:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('owners', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='employee',
            name='branch',
        ),
        migrations.AlterModelOptions(
            name='branch',
            options={'verbose_name': 'Sucursal'},
        ),
    ]
