from django.contrib.auth.models import User
from django.db import models


# Create your models here.

class Product(models.Model):
    name = models.CharField(max_length=255, default="")
    slug = models.SlugField(max_length=255, default="", unique=True)
    description = models.TextField(verbose_name="About", default="")
    price = models.FloatField(verbose_name="Price", default=0)
    user_like = models.ManyToManyField(User, blank=True, default="")
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Product"
        verbose_name_plural = "Products"
        ordering = ["name"]


class Comment(models.Model):
    product = models.ForeignKey(Product, verbose_name="Product")
    text = models.TextField(verbose_name="comment", default="")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text

    class Meta:
        verbose_name = "Comment"
        verbose_name_plural = "Comments"
        ordering = ["-created_at"]
