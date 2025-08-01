# Generated by Django 5.1.5 on 2025-02-15 10:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mandate', '0043_alter_mandate_ref'),
    ]

    operations = [
        migrations.AddField(
            model_name='mandate',
            name='debit_date',
            field=models.CharField(choices=[('3', '3rd day of month'), ('11', '11th day of month'), ('19', '19th day of month'), ('26', '26th day of month')], default='3', max_length=2, verbose_name='Date of EMI Collection'),
            preserve_default=False,
        ),
    ]
