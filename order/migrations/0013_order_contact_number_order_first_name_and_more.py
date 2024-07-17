# Generated by Django 4.2.7 on 2024-07-04 09:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0012_alter_order_payment_method'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='contact_number',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='order',
            name='first_name',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
        migrations.AddField(
            model_name='order',
            name='last_name',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
    ]