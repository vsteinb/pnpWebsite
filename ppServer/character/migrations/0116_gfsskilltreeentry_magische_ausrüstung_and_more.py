# Generated by Django 4.1.7 on 2023-07-25 19:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0059_alter_zauber_astralsch_is_direct'),
        ('character', '0115_alter_gfsskilltreeentry_operation'),
    ]

    operations = [
        migrations.AddField(
            model_name='gfsskilltreeentry',
            name='magische_ausrüstung',
            field=models.ForeignKey(blank=True, help_text='Für ein magisches Item', null=True, on_delete=django.db.models.deletion.SET_NULL, to='shop.magische_ausrüstung'),
        ),
        migrations.AddField(
            model_name='gfsskilltreeentry',
            name='wesenkraft',
            field=models.ForeignKey(blank=True, help_text='Für neue Wesenkraft', null=True, on_delete=django.db.models.deletion.SET_NULL, to='character.wesenkraft'),
        ),
        migrations.AlterField(
            model_name='gfsskilltreeentry',
            name='operation',
            field=models.CharField(choices=[('a', 'AP'), ('f', 'FP'), ('F', 'FG'), ('p', 'SP'), ('i', 'IP'), ('t', 'TP'), ('z', 'zauberslot'), ('v', 'neuer Vorteil'), ('n', 'neuer Nachteil'), ('x', 'Vorteil weg'), ('z', 'Nachteil weg'), ('e', 'neue Wesenkraft'), ('s', 'neue Spezialfertigkeit'), ('w', 'neue Wissensfertigkeit'), ('S', 'WP in Spezialfertigkeit'), ('W', 'WP in Wissensfertigkeit'), ('B', 'Bonus in Fertigkeit'), ('A', '+ Crit-Angriff'), ('V', '+ Crit-Verteidigung'), ('K', '+ körperliche HP'), ('G', '+ geistige HP'), ('k', 'Schaden waff. Kampf'), ('I', '+ Initiative fix'), ('r', 'Reaktion'), ('N', 'natürlicher Schadenswiderstand'), ('T', 'Astral-Widerstand'), ('h', 'magisches Item'), ('R', 'Roleplay-Text')], default='R', max_length=1),
        ),
    ]
