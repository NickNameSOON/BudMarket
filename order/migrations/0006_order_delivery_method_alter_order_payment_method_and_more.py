# Generated by Django 4.2.7 on 2024-04-09 15:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0005_order_payment_method'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='delivery_method',
            field=models.CharField(choices=[('pickup', 'Самовивіз з магазину'), ('delivery', 'Доставка')], default=1, max_length=20),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='order',
            name='payment_method',
            field=models.CharField(choices=[('cash', 'Готівка'), ('card', 'Карткою')], default='cash', max_length=20),
        ),
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('Опрацювання', 'Опрацювання'), ('packing', 'Комплектація'), ('delivering', 'Доставляється'), ('received', 'Отримано покупцем'), ('canceled', 'Відмінено')], default='Опрацювання', max_length=20),
        ),
    ]
