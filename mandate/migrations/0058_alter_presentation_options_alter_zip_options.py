# Generated by Django 5.1.5 on 2025-02-18 12:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mandate', '0057_alter_presentation_options_alter_zip_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='presentation',
            options={'get_latest_by': ['date', 'seq_no'], 'ordering': ['date', 'seq_no']},
        ),
        migrations.AlterModelOptions(
            name='zip',
            options={'get_latest_by': ['date', 'seq_no'], 'ordering': ['date', 'seq_no']},
        ),
    ]
