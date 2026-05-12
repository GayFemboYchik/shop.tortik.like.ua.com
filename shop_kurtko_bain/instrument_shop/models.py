from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify


# Create your models here.
class Category(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True, null=True)  # Додайте це

    def save(self, *args, **kwargs):
        if not self.slug:
            from django.utils.text import slugify
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class Subcategory(models.Model):
    title = models.CharField(max_length=200)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    slug = models.SlugField(unique=True, blank=True, null=True)  # І це теж

    def save(self, *args, **kwargs):
        if not self.slug:
            from django.utils.text import slugify
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
    def __str__(self):
        return self.title

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
        ('cart', 'У кошику'),  # товар ще у кошику, не оформлено
        ('processing', 'Обробляється'),  # замовлення прийнято, йде обробка
        ('confirmed', 'Підтверджено'),  # замовлення підтверджено менеджером
        ('completed', 'Виконано'),  # замовлення виконано / доставлено
    ]

    @property
    def total_price(self):
        return sum(item.total_price for item in self.items.all())

    client = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='cart'  # замовлення початково у кошику
    )


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    instrument = models.ForeignKey(Instrument, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    @property
    def total_price(self):
        # ціна одного інструмента * кількість
        return self.instrument.price * self.quantity


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    avatar = models.ImageField(upload_to='profiles/', blank=True, null=True)

    def __str__(self):
        return f"Профіль: {self.user.username}"
