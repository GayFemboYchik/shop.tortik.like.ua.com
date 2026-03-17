from django.db import models
from django.contrib.auth.models import AbstractUser

class Client(AbstractUser):
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True)


    def __str__(self):
        return self.username


# Create your models here.
class Category(models.Model):
    title = models.CharField(max_length=200)
    def __str__(self):
        return self.title

class Subcategory(models.Model):
    title = models.CharField(max_length=200)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

from django.utils.text import slugify

from django.utils.text import slugify

class Instrument(models.Model):
    title = models.CharField(max_length=200)
    subcategory = models.ForeignKey(Subcategory, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    in_stock = models.PositiveIntegerField()
    description = models.TextField()
    image = models.ImageField(upload_to='instruments/', blank=True, null=True)
    slug = models.SlugField(unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class Order(models.Model):
    STATUS_CHOICES = [
        ('cart', 'У кошику'),          # товар ще у кошику, не оформлено
        ('processing', 'Обробляється'), # замовлення прийнято, йде обробка
        ('confirmed', 'Підтверджено'),  # замовлення підтверджено менеджером
        ('completed', 'Виконано'),      # замовлення виконано / доставлено
    ]

    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='cart'   # замовлення початково у кошику
    )

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    instrument = models.ForeignKey(Instrument, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)








