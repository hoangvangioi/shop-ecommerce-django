from django.db import models
from django.urls import reverse

# Create your models here.


class Category(models.Model):
    category_name  = models.CharField(max_length=50, unique=True)
    slug           = models.SlugField(max_length=100, unique=True)
    description    = models.TextField(max_length=255, blank=True)
    category_image = models.ImageField(upload_to='categories', blank=True)

    class Meta:
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def get_absolute_url(self):
            return reverse('products_by_category', args=[self.slug])

    def __str__(self):
        return self.category_name
    
    


class CategoryBlog(models.Model):
    category_blog_name  = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=100, unique=True)

    class Meta:
        verbose_name = 'category blog'
        verbose_name_plural = 'categories blog'

    def get_absolute_url(self):
            return reverse('blog_by_category', args=[self.slug])

    def __str__(self):
        return self.category_blog_name