# Generated by Django 3.1.6 on 2021-02-13 17:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('aeg', '0004_essays_evaluated'),
    ]

    operations = [
        migrations.CreateModel(
            name='Report',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('report', models.FileField(upload_to='Essays/Report/')),
                ('essay', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='aeg.essays')),
            ],
        ),
    ]