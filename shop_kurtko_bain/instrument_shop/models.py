from django.db import models

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

class Instrument(models.Model):
    title = models.CharField(max_length=200)
    subcategory = models.ForeignKey(Subcategory, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    in_stock = models.PositiveIntegerField()
    description = models.TextField()
    def __str__(self):
        return self.title
class Order(models.Model):
    title = models.CharField(max_length=200)
    instrument = models.ForeignKey(Instrument, on_delete=models.CASCADE)




class Client(models.Model):
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    email = models.EmailField()




