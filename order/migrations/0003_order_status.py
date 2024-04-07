# Generated by Django 4.2.7 on 2024-04-07 03:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0002_alter_order_total_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('processing', 'Опрацювання'), ('packing', 'Комплектація'), ('delivering', 'Доставляється'), ('received', 'Отримано покупцем'), ('canceled', 'Відмінено')], default='processing', max_length=20),
        ),
    ]
