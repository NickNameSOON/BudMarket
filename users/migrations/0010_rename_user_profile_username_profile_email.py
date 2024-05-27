# Generated by Django 4.2.7 on 2024-04-08 03:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0009_alter_profile_cart_delete_userregister'),
    ]

    operations = [
        migrations.RenameField(
            model_name='profile',
            old_name='user',
            new_name='username',
        ),
        migrations.AddField(
            model_name='profile',
            name='email',
            field=models.EmailField(default=1, max_length=100, unique=True),
            preserve_default=False,
        ),
    ]