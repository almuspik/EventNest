# Generated by Django 4.2.4 on 2025-07-13 08:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0006_venue_venue_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='approved',
            field=models.BooleanField(default=True, verbose_name='Approved'),
        ),
    ]
