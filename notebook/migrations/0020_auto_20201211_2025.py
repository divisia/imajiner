# Generated by Django 3.1.4 on 2020-12-11 17:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notebook', '0019_auto_20201211_1613'),
    ]

    operations = [
        migrations.AddField(
            model_name='narrative',
            name='public',
            field=models.BooleanField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='narrativetranslation',
            name='public',
            field=models.BooleanField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='narrativeversion',
            name='public',
            field=models.BooleanField(blank=True, null=True),
        ),
    ]
