# Generated by Django 4.1.6 on 2023-03-02 21:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='data_joined',
            new_name='date_joined',
        ),
    ]
