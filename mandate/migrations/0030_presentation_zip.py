# Generated by Django 5.1.5 on 2025-02-07 11:46

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mandate', '0029_zip_presentation'),
    ]

    operations = [
        migrations.AddField(
            model_name='presentation',
            name='zip',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='mandate.zip'),
        ),
    ]
