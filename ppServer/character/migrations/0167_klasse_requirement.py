# Generated by Django 4.2.8 on 2024-11-02 10:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('character', '0166_charakter_klassen_charakter_klassen_fähigkeiten_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='klasse',
            name='requirement',
            field=models.CharField(blank=True, help_text='Hat keine Auswirkungen, ist nur zum Anzeigen', max_length=128, null=True),
        ),
    ]
