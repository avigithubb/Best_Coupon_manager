from django.db import models
import uuid

# Create your models here.

class Coupons(models.Model):
    code = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True)
    discountType = models.CharField(max_length=20)
    discountValue = models.DecimalField(max_digits=10, decimal_places=2)
    maxDiscountAmount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    startDate = models.DateTimeField()
    endDate = models.DateTimeField()
    usageLimitPerUser = models.IntegerField(null=True, blank=True)
    eligibility = models.CharField(max_length=100, blank=True)
    uuid = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)

    def __str__(self):
        return self.code

class CartItems(models.Model):
    productId = models.CharField(max_length=50)
    unitPrice = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(max_length=50)
    quantity = models.IntegerField(default=1)
    user = models.ForeignKey('User', on_delete=models.CASCADE, related_name='cart_items')

    class Meta:
        unique_together = ('productId', 'user')

    def __str__(self):
        return f"{self.productId} x {self.quantity}"
    
class User(models.Model):
    userTier = models.CharField(max_length=20)
    country = models.CharField(max_length=50)
    lifetimeSpend = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    ordersPlaced = models.IntegerField(default=0)


