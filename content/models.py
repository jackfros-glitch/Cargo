from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    
    def __str__(self):
        return self.name
    
class Tag(models.Model):
    name = models.CharField(max_length=200)
    
    def __str__(self):
        return self.name


# Create your models here.
class Content(models.Model):
    owner = models.ForeignKey(User, on_delete= models.CASCADE, related_name='contents')
    title = models.CharField(max_length=200)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete = models.CASCADE, related_name='contents')
    tags = models.ManyToManyField(Tag, related_name='contents')
    ai_relevance_score = models.FloatField(default=0.0)
    
    def __str__(self):
        return self.title