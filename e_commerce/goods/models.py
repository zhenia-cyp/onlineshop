from django.db import models
from django.urls import reverse

class Category(models.Model):

    name = models.CharField(max_length=150)
    slug = models.SlugField(max_length=200, unique=True, blank=True, null=True)


    class Meta:
        
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
        ordering = ['name']

    def __str__(self):
        return f"{self.name}"
    


class Product(models.Model):

    name = models.CharField(max_length=150, unique=True)
    slug = models.SlugField(max_length=200, unique=True, blank=True, null=True, verbose_name='URL')
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='goods_images', blank=True, null=True)
    price = models.DecimalField(default=0.00, max_digits=7, decimal_places=2)
    discount = models.DecimalField(default=0.00, max_digits=4, decimal_places=2)
    quantity = models.PositiveIntegerField(default=0)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


    class Meta:
        
        db_table = 'product'
        verbose_name = 'Product'
        verbose_name_plural = 'Products'
        ordering = ("-id",)

    def __str__(self):
        return f'{self.name} quantity - {self.quantity}'

    def get_absolute_url(self):
        return reverse("catalog:product", kwargs={"slug": self.slug})

    def display_id(self):
        return f'{self.id:05}'
    
    def sell_price(self):
        if self.discount:
            result_price = round(self.price - self.price*self.discount/100, 2)
            if result_price <= 0:  
                return None 
            return result_price
        
        return self.price