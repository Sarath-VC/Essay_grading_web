# Generated by Django 3.1.6 on 2021-02-13 16:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('aeg', '0003_essays_topic'),
    ]

    operations = [
        migrations.AddField(
            model_name='essays',
            name='evaluated',
            field=models.BooleanField(default=False),
        ),
    ]