# Generated by Django 4.2.7 on 2024-07-20 13:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('market', '0025_remove_product_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='image',
            field=models.ImageField(blank=True, upload_to='products/%Y/%m/%d', verbose_name='Титульне зображення'),
        ),
    ]
