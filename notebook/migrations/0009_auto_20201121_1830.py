# Generated by Django 3.1.2 on 2020-11-21 15:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notebook', '0008_auto_20201121_1414'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='narrative',
            options={'ordering': ('-created_at',)},
        ),
        migrations.RemoveField(
            model_name='narrative',
            name='versioning',
        ),
        migrations.AddField(
            model_name='narrative',
            name='edited_at',
            field=models.DateTimeField(auto_now=True, verbose_name='Last edited at'),
        ),
        migrations.AlterField(
            model_name='narrative',
            name='language',
            field=models.CharField(blank=True, choices=[('en', 'English'), ('tr', 'Türkçe'), ('fr', 'Français'), ('de', 'Deustch'), ('ru', 'русский')], max_length=5, null=True),
        ),
        migrations.AlterField(
            model_name='narrativetranslation',
            name='language',
            field=models.CharField(choices=[('en', 'English'), ('tr', 'Türkçe'), ('fr', 'Français'), ('de', 'Deustch'), ('ru', 'русский')], max_length=5),
        ),
    ]