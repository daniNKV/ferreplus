# Generated by Django 5.0.4 on 2024-05-14 20:14

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("item", "0004_item_wastraded_alter_category_name_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="item",
            name="image",
            field=models.ImageField(upload_to="media/item"),
        ),
    ]
