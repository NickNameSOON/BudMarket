# Generated by Django 4.2.7 on 2024-07-08 14:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('market', '0020_alter_banner_alt'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Banner',
            new_name='HomeImage',
        ),
    ]