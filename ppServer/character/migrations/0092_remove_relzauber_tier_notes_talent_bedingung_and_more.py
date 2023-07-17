# Generated by Django 4.1.7 on 2023-07-17 13:29

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('character', '0091_alter_charakter_zauberplätze_gfszauber'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='relzauber',
            name='tier_notes',
        ),
        migrations.AddField(
            model_name='talent',
            name='bedingung',
            field=models.ManyToManyField(to='character.talent'),
        ),
        migrations.AlterField(
            model_name='gfszauber',
            name='tier',
            field=models.PositiveSmallIntegerField(default=0, validators=[django.core.validators.MaxValueValidator(7)]),
        ),
    ]
