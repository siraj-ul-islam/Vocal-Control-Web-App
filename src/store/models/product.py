from django.db import models
from .category import Category

class Color(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
class Products(models.Model):
    name = models.CharField(max_length=60)
    price= models.IntegerField(default=0)
    in_stock = models.IntegerField(null=True, blank=True)

    color = models.ManyToManyField(Color, null=True, blank=True)
    class S(models.TextChoices):
        S = 'S', 'S'
        M = 'M', 'M'
        L = 'L', 'L'
        XL = 'XL', 'XL'
    
    size = models.CharField(max_length=2, choices=S.choices, default=S.S, null=True, blank=True)
    show_sizes = models.BooleanField(default=False)
    show_colors = models.BooleanField(default=False)
    category= models.ForeignKey(Category,on_delete=models.CASCADE,default=1 ) # type: ignore
    description= models.CharField(max_length=250, default='', blank=True, null= True)
    image= models.ImageField(upload_to='uploads/products/')

    @staticmethod
    def get_products_by_id(ids):
        return Products.objects.filter (id__in=ids)
    @staticmethod
    def get_all_products():
        return Products.objects.all()

    @staticmethod
    def get_all_products_by_categoryid(category_id):
        if category_id:
            return Products.objects.filter (category=category_id)
        else:
            return Products.get_all_products();