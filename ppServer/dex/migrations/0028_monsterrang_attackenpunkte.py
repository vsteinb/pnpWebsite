# Generated by Django 4.2.8 on 2023-12-22 13:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dex', '0027_attacke_cost'),
    ]

    operations = [
        migrations.AddField(
            model_name='monsterrang',
            name='attackenpunkte',
            field=models.PositiveSmallIntegerField(default=0),
        ),
    ]
