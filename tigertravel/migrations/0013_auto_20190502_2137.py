# Generated by Django 2.1.7 on 2019-05-02 21:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tigertravel', '0012_auto_20190502_2127'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comment',
            name='created_date',
        ),
        migrations.AlterField(
            model_name='comment',
            name='text',
            field=models.TextField(default='message'),
        ),
    ]
