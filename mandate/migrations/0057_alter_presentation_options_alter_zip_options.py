# Generated by Django 5.1.5 on 2025-02-18 12:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mandate', '0056_alter_presentation_npci_status'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='presentation',
            options={'get_latest_by': ['date', 'seq'], 'ordering': ['date', 'seq_no']},
        ),
        migrations.AlterModelOptions(
            name='zip',
            options={'get_latest_by': ['date', 'seq'], 'ordering': ['date', 'seq_no']},
        ),
    ]
