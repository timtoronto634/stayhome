# Generated by Django 3.0.5 on 2020-05-15 13:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wordwolves', '0004_player_plain_pass'),
    ]

    operations = [
        migrations.AddField(
            model_name='player',
            name='replay',
            field=models.BooleanField(default=False),
        ),
    ]