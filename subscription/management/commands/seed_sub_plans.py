from django.core.management.base import BaseCommand
from subscription.models import SubscriptionPlan

class Command(BaseCommand):
    help = "Seed initial subscription plans"

    def handle(self, *args, **kwargs):
        plans = [
            {"name": "monthly", "price": 10.00, "duration_days": 30},
            {"name": "quarterly", "price": 25.00, "duration_days": 90},
            {"name": "bi_yearly", "price": 45.00, "duration_days": 180},
            {"name": "yearly", "price": 80.00, "duration_days": 365},
        ]
        for plan_data in plans:
            SubscriptionPlan.objects.get_or_create(**plan_data)
        self.stdout.write(self.style.SUCCESS("Subscription plans seeded successfully"))