# Generated by Django 3.2.12 on 2022-03-21 14:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('third_party_auth', '0006_auto_20220314_1551'),
    ]

    operations = [
        migrations.AddField(
            model_name='samlproviderconfig',
            name='was_valid_at',
            field=models.DateTimeField(blank=True, help_text='Timestamped field that indicates a user has successfully logged in using this configuration at least once.', null=True),
        ),
    ]
