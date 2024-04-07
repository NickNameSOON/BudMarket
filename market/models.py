from django.db import models
from django.utils.text import slugify
import random
import string
from django.urls import reverse


def rand_slug():
    """
    Generates a random slug consisting of lowercase letters and digits.

    Returns:
        str: The randomly generated slug.
    """
    return '>'.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(3))


class Category(models.Model):
    """
    Represents a category in the marketplace.

    """
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


class Product(models.Model):
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE, null=True)
    title = models.CharField("назва", max_length=200, db_index=True)
    slug = models.SlugField("URL", max_length=200, db_index=True, null=True, blank=True)
    brand = models.CharField("бренд", max_length=200, db_index=True, null=True, blank=True)
    image = models.ImageField("зображення", upload_to='products/%Y/%m/%d', blank=True)
    description = models.TextField("опис", null=True, blank=True)
    price = models.DecimalField('ціна', max_digits=10, decimal_places=2)
    available = models.BooleanField("Наявність", default=True)

    def get_price(self):
        return self.price

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товари'

    def __str__(self):
        """
        Returns a string representation of the object.
        """
        return self.title


class ProductManager(models.Manager):
    def get_queryset(self):
        return super(ProductManager, self).get_queryset().filter(available=True)


class ProductProxy(Product):

    objects = ProductManager()

    class Meta:
        proxy = True