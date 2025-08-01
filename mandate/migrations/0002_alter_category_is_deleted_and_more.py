# Generated by Django 5.1.3 on 2024-12-05 12:05

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mandate', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='is_deleted',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='debtoracctype',
            name='is_deleted',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='debtorbank',
            name='is_deleted',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='frequency',
            name='is_deleted',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='paymenttype',
            name='is_deleted',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='variant',
            name='is_deleted',
            field=models.BooleanField(default=False),
        ),
        migrations.CreateModel(
            name='Mandate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('umrn', models.CharField(max_length=50)),
                ('message_reference', models.CharField(max_length=100)),
                ('currency', models.CharField(max_length=5)),
                ('fixed_or_max', models.CharField(max_length=1)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('date_of_mandate', models.DateField()),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('name_of_debtor_account_holder', models.CharField(max_length=300)),
                ('debtor_legal_account_number', models.CharField(max_length=100)),
                ('creditor_name', models.CharField(max_length=300)),
                ('creditor_bank', models.CharField(default='SARVA HARYANA GRAMIN BANK', max_length=300)),
                ('creditor_utility_code', models.CharField(default='HGBX00002000017848', max_length=100)),
                ('mandate_image', models.ImageField(null=True, upload_to='')),
                ('mandate_file', models.FileField(null=True, upload_to='')),
                ('is_deleted', models.BooleanField(default=False)),
                ('image_uploaded', models.BooleanField(default=False)),
                ('locked', models.BooleanField(default=False)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='mandate.category')),
                ('debtor_acc_type', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='mandate.debtoracctype')),
                ('debtor_bank', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='mandate.debtorbank')),
                ('frequency', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='mandate.frequency')),
                ('variant', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='mandate.variant')),
            ],
        ),
    ]
