# Generated by Django 5.1.5 on 2025-02-27 05:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mandate', '0063_mandate_init_req_flag'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='mandate',
            name='init_count',
        ),
    ]
