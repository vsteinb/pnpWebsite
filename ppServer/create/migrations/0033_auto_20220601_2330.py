# Generated by Django 3.1.7 on 2022-06-01 21:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('character', '0062_charakter_begleiter'),
        ('create', '0032_newcharakter_spf_wf'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='NewCharacterPersönlichkeit',
            new_name='NewCharakterPersönlichkeit',
        ),
        migrations.AlterField(
            model_name='newcharakter',
            name='profession',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='character.profession'),
        ),
    ]
