# Generated by Django 4.2.7 on 2024-03-30 19:41

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('market', '0013_remove_product_created_at_remove_product_upload_at'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='upload_at',
        ),
        migrations.AddField(
            model_name='category',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now, verbose_name='Дата створення'),
            preserve_default=False,
        ),
    ]
