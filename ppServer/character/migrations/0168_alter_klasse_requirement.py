# Generated by Django 4.2.8 on 2024-11-02 12:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('character', '0167_klasse_requirement'),
    ]

    operations = [
        migrations.AlterField(
            model_name='klasse',
            name='requirement',
            field=models.CharField(blank=True, help_text='Wird auch halbwegs zur Berechnung benutzt, also bitte nicht selbstständig ändern!', max_length=128, null=True),
        ),
    ]
