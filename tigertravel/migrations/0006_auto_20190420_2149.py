# Generated by Django 2.1.7 on 2019-04-20 21:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tigertravel', '0005_request_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='group',
            name='members',
            field=models.ManyToManyField(to='tigertravel.Request'),
        ),
    ]
