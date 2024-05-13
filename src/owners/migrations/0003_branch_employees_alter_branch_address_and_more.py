# Generated by Django 5.0.6 on 2024-05-12 13:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('owners', '0002_remove_employee_branch_alter_branch_options'),
        ('user', '0002_alter_user_options_alter_user_birth_date_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='branch',
            name='employees',
            field=models.ManyToManyField(related_name='branches', to='user.employee', verbose_name='empleados'),
        ),
        migrations.AlterField(
            model_name='branch',
            name='address',
            field=models.CharField(max_length=100, verbose_name='direccion'),
        ),
        migrations.AlterField(
            model_name='branch',
            name='closing_hour',
            field=models.TimeField(verbose_name='hora de cierre'),
        ),
        migrations.AlterField(
            model_name='branch',
            name='name',
            field=models.CharField(max_length=100, verbose_name='nombre'),
        ),
        migrations.AlterField(
            model_name='branch',
            name='opening_hour',
            field=models.TimeField(verbose_name='hora de apertura'),
        ),
        migrations.DeleteModel(
            name='Employee',
        ),
    ]
