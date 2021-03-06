# Generated by Django 3.1.2 on 2020-11-18 13:14

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('identity', '0005_loggedinuser'),
    ]

    operations = [
        migrations.AlterField(
            model_name='loggedinuser',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='logged_in', to=settings.AUTH_USER_MODEL),
        ),
    ]
