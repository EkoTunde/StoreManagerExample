# Generated by Django 2.2.2 on 2021-04-29 20:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='is_manager',
            field=models.BooleanField(default=False),
        ),
    ]