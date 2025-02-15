# Generated by Django 4.2.8 on 2024-12-18 19:48

from django.db import migrations
import markdownfield.models


class Migration(migrations.Migration):

    dependencies = [
        ('character', '0175_charakter_pfeile_bolzen'),
    ]

    operations = [
        migrations.AddField(
            model_name='gfs',
            name='eigenschaften',
            field=markdownfield.models.MarkdownField(default='-', rendered_field='eigenschaften_rendered'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='gfs',
            name='eigenschaften_rendered',
            field=markdownfield.models.RenderedMarkdownField(null=True),
        ),
    ]
