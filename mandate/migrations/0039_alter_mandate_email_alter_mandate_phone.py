# Generated by Django 5.1.5 on 2025-02-14 07:42

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mandate', '0038_mandate_email_mandate_phone_alter_mandate_debit_type_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mandate',
            name='email',
            field=models.EmailField(blank=True, max_length=254, null=True, verbose_name='Customer EMail ID'),
        ),
        migrations.AlterField(
            model_name='mandate',
            name='phone',
            field=models.CharField(blank=True, max_length=10, null=True, validators=[django.core.validators.RegexValidator(code='invalid_phone', message='The phone number is invalid', regex='^\\d{10}$')], verbose_name='Customer Mobile No.'),
        ),
    ]
