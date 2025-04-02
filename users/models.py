from django.db import models
from django.contrib.auth.models import User

from content.models import Content


# Create your models here.
class UserActivity(models.Model):
    ACTION_CHOICES = [
        ("viewed", "Viewed"),
        ("liked", "Liked"),
        ("skipped", "Skipped"),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    action = models.CharField(max_length=10, choices=ACTION_CHOICES)
    content = models.ForeignKey(Content, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f"{self.user.username} {self.action} content {self.content.title}"