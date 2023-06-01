from django.db import models


# Create your models here.
class Registration(models.Model):
    first_name = models.CharField(max_length=50, null=True, blank=True)
    last_name = models.CharField(max_length=50, null=True, blank=True)
    email = models.EmailField(max_length=50, null=True, blank=True)
    password = models.CharField(max_length=255, null=True, blank=True)
    mobile = models.CharField(max_length=15, null=True, blank=True)
    gender = models.CharField(max_length=50)

    def __str__(self):
        return self.first_name


class Category(models.Model):
    cat_name = models.CharField(max_length=50, null=True, blank=True)
    cat_image = models.ImageField(upload_to="category/")

    def __str__(self):
        return self.cat_name


class Product(models.Model):
    product_name = models.CharField(max_length=50, null=True, blank=True)
    product_image = models.ImageField(upload_to="product/")
    product_description = models.CharField(max_length=50, null=True, blank=True)
    product_price = models.IntegerField(null=True, blank=True)
    product_category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return self.product_name


class Order(models.Model):
    address = models.CharField(max_length=250, default="", null=True)
    mobile = models.BigIntegerField()
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    price = models.IntegerField()
    customer = models.ForeignKey(Registration, on_delete=models.CASCADE)
    status = models.BooleanField(default="False")

    def __str__(self):
        return self.product.product_name
