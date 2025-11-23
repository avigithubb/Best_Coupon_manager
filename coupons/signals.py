from django.contrib.auth import get_user_model
from django.db.models.signals import post_migrate
from django.dispatch import receiver

User = get_user_model()

@receiver(post_migrate)
def create_demo_user(sender, **kwargs):
    if not User.objects.filter(email="hire-me@anshumat.org").exists():
        User.objects.create_user(
            username="hire-me",
            email="hire-me@anshumat.org",
            password="HireMe@2025!"
        )
        print("Demo user created: hire-me@anshumat.org / HireMe@2025!")