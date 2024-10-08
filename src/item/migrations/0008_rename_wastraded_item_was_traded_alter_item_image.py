# Generated by Django 5.0.3 on 2024-05-15 22:02

import core.jobs
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("item", "0007_item_branch_item_user"),
    ]

    operations = [
        migrations.RenameField(
            model_name="item",
            old_name="wasTraded",
            new_name="was_traded",
        ),
        migrations.AlterField(
            model_name="item",
            name="image",
            field=models.ImageField(
                upload_to=core.jobs.UploadToPathAndRename("item/images/")
            ),
        ),
    ]
