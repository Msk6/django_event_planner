# Generated by Django 2.2.5 on 2020-09-20 16:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0002_booking'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='reserved_seats',
            field=models.IntegerField(default=6),
            preserve_default=False,
        ),
    ]