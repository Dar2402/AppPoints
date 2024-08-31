from django.db import models
from django.utils import timezone

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(default=timezone.now)
    created_by = models.ForeignKey('user_app.User', related_name='categories', on_delete=models.CASCADE)
    
    def __str__(self):
        return self.name

class Subcategory(models.Model):
    category = models.ForeignKey(Category, related_name='subcategories', on_delete=models.CASCADE)
    name = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(default=timezone.now)
    created_by = models.ForeignKey('user_app.User', related_name='subcategories', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.category.name} - {self.name}'

class App(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    points = models.PositiveIntegerField()
    category = models.ForeignKey(Category, related_name='apps', on_delete=models.CASCADE)
    subcategory = models.ForeignKey(Subcategory, related_name='apps', on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)
    created_by = models.ForeignKey('user_app.User', related_name='apps', on_delete=models.CASCADE)

    def __str__(self):
        return self.name