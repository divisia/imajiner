# Generated by Django 3.1.2 on 2020-11-05 16:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notebook', '0002_auto_20201030_0318'),
    ]

    operations = [
        migrations.AddField(
            model_name='narrative',
            name='published_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
