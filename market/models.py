from django.db import models
from django.utils.text import slugify
import random
import string


def rand_slug():
    return ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(3))


class Category(models.Model):
    name = models.CharField(max_length=200, db_index=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, related_name='children', null=True, blank=True)
    slug = models.SlugField('URL', max_length=200, unique=True, db_index=True, null=True, blank=True)
    created_at = models.DateTimeField('Дата створення', auto_now_add=True)

    class Meta:
        unique_together = (['name', 'parent'])
        verbose_name = 'Категорія'
        verbose_name_plural = 'Категорії'

    def __str__(self):
        full_path = [self.name]
        k = self.parent
        while k is not None:
            full_path.append(k.name)
            k = k.parent
        return '>'.join(full_path[::-1])

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(rand_slug() + '-pickBetter' + self.name)
        super(Category, self).save(*args, **kwargs)


class ProductAttribute(models.Model):
    name = models.CharField(max_length=200)
    category = models.ForeignKey(Category, related_name='attributes', on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Характеристика товару'
        verbose_name_plural = 'Характеристики товарів'

    def __str__(self):
        return self.name


class Product(models.Model):
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE, null=True)
    title = models.CharField("назва", max_length=200, db_index=True)
    slug = models.SlugField("URL", max_length=200, db_index=True, null=True, blank=True)
    brand = models.CharField("бренд", max_length=200, db_index=True, null=True, blank=True)
    image = models.ImageField("Титульне зображення", upload_to='products/%Y/%m/%d', blank=True)
    description = models.TextField("опис", null=True, blank=True)
    price = models.DecimalField('ціна', max_digits=10, decimal_places=2)
    available = models.BooleanField("Наявність", default=True)

    def get_price(self):
        return self.price

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товари'

    def __str__(self):
        return self.title


class ProductAttributeValue(models.Model):
    product = models.ForeignKey(Product, related_name='attribute_values', on_delete=models.CASCADE)
    attribute = models.ForeignKey(ProductAttribute, related_name='values', on_delete=models.CASCADE)
    value = models.CharField(max_length=200)

    class Meta:
        verbose_name = 'Значення характеристики товару'
        verbose_name_plural = 'Значення характеристик товарів'

    def __str__(self):
        return f'{self.attribute.name}: {self.value}'


# models.py

class HomeImage(models.Model):
    image = models.ImageField("Зображення", upload_to='banners/%Y/%m/%d')
    alt = models.CharField("Альтернативний текст", max_length=200)
    order = models.PositiveIntegerField("Порядок", default=0)
    url = models.URLField("URL", max_length=200, blank=True, null=True, default='#')

    class Meta:
        ordering = ['order']
        verbose_name = 'Банер'
        verbose_name_plural = 'Банери'

    def __str__(self):
        return self.alt


class ProductImage(models.Model):
    product = models.ForeignKey(Product, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='products/%Y/%m/%d')

    def __str__(self):
        return f"{self.product.title} Image"
