# Generated by Django 3.0 on 2019-12-04 11:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0002_ticket'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='event_url',
            field=models.URLField(default='', verbose_name='event url'),
            preserve_default=False,
        ),
    ]
