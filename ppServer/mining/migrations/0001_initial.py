# Generated by Django 3.1.5 on 2021-04-25 12:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('shop', '0041_auto_20201111_2045'),
    ]

    operations = [
        migrations.CreateModel(
            name='Material',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('icon', models.ImageField(upload_to='')),
                ('rigidity', models.PositiveIntegerField(default=10)),
                ('tier', models.PositiveIntegerField(default=0)),
            ],
            options={
                'verbose_name': 'Material',
                'verbose_name_plural': 'Materialien',
            },
        ),
        migrations.CreateModel(
            name='Region',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, unique=True)),
                ('field', models.TextField(default='[[]]')),
            ],
            options={
                'verbose_name': 'Region',
                'verbose_name_plural': 'Regionen',
            },
        ),
        migrations.CreateModel(
            name='MaterialDrop',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.TextField(default='[1]')),
                ('item', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='shop.tinker')),
                ('material', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mining.material')),
            ],
        ),
    ]
