# Generated by Django 4.2.8 on 2024-09-25 15:18

from django.db import migrations, models

def migrate_language(apps, schema_editor):
    Spieler = apps.get_model('character', 'Spieler')

    Spieler.objects.filter(language_daemonisch=True).update(language="d")


class Migration(migrations.Migration):

    dependencies = [
        ('character', '0153_alter_charakter_notizen_sonstiger_manifestverlust_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='spieler',
            name='language',
            field=models.CharField(choices=[('g', 'Gemeinsprache'), ('d', 'Dämonisch'), ('e', 'Hochelfisch')], default='g', max_length=1, verbose_name='Sprache'),
        ),
        migrations.RunPython(migrate_language)
    ]
