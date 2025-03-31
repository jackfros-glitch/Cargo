from django.db import models
from django.contrib.auth import get_user_model
from datetime import timedelta, datetime
from django.utils import timezone

User = get_user_model()

class SubscriptionPlan(models.Model):
    PLAN_CHOICES = [
        ('monthly', 'Monthly'),
        ('quarterly', 'Quarterly'),
        ('bi_yearly', 'Bi-Yearly'),
        ('yearly', 'Yearly'),
    ]

    name = models.CharField(max_length=50, choices=PLAN_CHOICES, unique=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    duration_days = models.IntegerField()  # Store duration in days

    def __str__(self):
        return f"{self.name} - ${self.price}"

class Subscription(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="subscription")
    plan = models.ForeignKey(SubscriptionPlan, on_delete=models.CASCADE)
    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField()
    auto_renew = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if not self.start_date:
            self.start_date = timezone.now()  
        if not self.end_date:
            self.end_date = self.start_date + timedelta(days=self.plan.duration_days)
        super().save(*args, **kwargs)

    def is_active(self):
        return self.end_date >= datetime.now()
