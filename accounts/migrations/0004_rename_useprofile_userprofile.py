# Generated by Django 4.1.6 on 2023-03-02 21:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_useprofile'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='UseProfile',
            new_name='UserProfile',
        ),
    ]
