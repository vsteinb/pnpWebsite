# Generated by Django 2.2.13 on 2020-12-19 12:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('time_space', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='net',
            name='text',
            field=models.TextField(blank=True, null=True),
        ),
    ]
