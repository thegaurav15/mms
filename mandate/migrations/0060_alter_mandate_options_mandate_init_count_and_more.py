# Generated by Django 5.1.5 on 2025-02-25 12:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mandate', '0059_alter_presentation_filename_prefix_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='mandate',
            options={'ordering': ['-id']},
        ),
        migrations.AddField(
            model_name='mandate',
            name='init_count',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='mandate',
            name='last_init_req_time',
            field=models.DateTimeField(null=True),
        ),
        migrations.AlterField(
            model_name='mandate',
            name='mandate_image',
            field=models.ImageField(null=True, upload_to='mandate/images/mandate/%Y/%m/%d/', verbose_name='Mandate Image'),
        ),
    ]
