from django.contrib import admin

# Register your models here.
from django.contrib.admin.options import InlineModelAdmin

from product.models import Product, Comment


class CommentInline(admin.TabularInline):
    model = Comment
    extra = 1


class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    inlines = [CommentInline, ]


admin.site.register(Product, ProductAdmin)
