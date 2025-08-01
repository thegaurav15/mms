# Generated by Django 5.1.3 on 2024-12-06 05:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mandate', '0002_alter_category_is_deleted_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mandate',
            name='mandate_file',
            field=models.FileField(blank=True, null=True, upload_to=''),
        ),
        migrations.AlterField(
            model_name='mandate',
            name='mandate_image',
            field=models.ImageField(null=True, upload_to='mandate/images/'),
        ),
    ]
