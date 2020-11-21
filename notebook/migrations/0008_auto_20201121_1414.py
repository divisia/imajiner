# Generated by Django 3.1.2 on 2020-11-21 11:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notebook', '0007_auto_20201121_1324'),
    ]

    operations = [
        migrations.AlterField(
            model_name='narrative',
            name='language',
            field=models.CharField(blank=True, choices=[('en', 'English'), ('tr', 'Türkçe')], max_length=5, null=True),
        ),
        migrations.AlterField(
            model_name='narrative',
            name='sketch',
            field=models.BooleanField(default=True, verbose_name='Sketch'),
        ),
        migrations.AlterField(
            model_name='narrativetranslation',
            name='language',
            field=models.CharField(choices=[('en', 'English'), ('tr', 'Türkçe')], max_length=5),
        ),
    ]
