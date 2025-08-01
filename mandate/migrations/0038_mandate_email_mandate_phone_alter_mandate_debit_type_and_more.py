# Generated by Django 5.1.5 on 2025-02-14 07:32

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mandate', '0037_presentation_npci_upload_error_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='mandate',
            name='email',
            field=models.EmailField(blank=True, max_length=254, null=True),
        ),
        migrations.AddField(
            model_name='mandate',
            name='phone',
            field=models.CharField(blank=True, max_length=10, null=True, validators=[django.core.validators.RegexValidator(code='invalid_phone', message='The phone number is invalid', regex='^\\d{10}$')], verbose_name='Mobile'),
        ),
        migrations.AlterField(
            model_name='mandate',
            name='debit_type',
            field=models.CharField(choices=[(None, ''), ('F', 'Fixed Amount'), ('M', 'Max Amount')], default='F', max_length=1, verbose_name='Debit Type'),
        ),
        migrations.AlterField(
            model_name='mandate',
            name='frequency',
            field=models.CharField(choices=[(None, ''), ('ADHO', 'As and when presented'), ('INDA', 'Intra Day'), ('DAIL', 'Daily'), ('WEEK', 'Weekly'), ('BIMN', 'Bi-Monthly'), ('MNTH', 'Monthly '), ('QURT', 'Quaterly'), ('MIAN', 'Semi annually'), ('YEAR', 'Yearly')], default='MNTH', max_length=4, verbose_name='Frequency'),
        ),
    ]
