# Generated by Django 2.2.13 on 2020-12-19 13:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('time_space', '0002_net_text'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='net',
            name='startNodeId',
        ),
        migrations.AddField(
            model_name='net',
            name='startNode',
            field=models.TextField(blank=True, null=True),
        ),
    ]
