from ..models import Coupons, CartItems, User
from rest_framework import serializers

class CouponSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coupons
        fields = ["code", "description", "discountType", "discountValue", "maxDiscountAmount", "startDate", "endDate", "usageLimitPerUser", "eligibility"]
    
class CartItemSerializer(serializers.Serializer):
    class Meta:
        model = CartItems
        fields = ["productId", "unitPrice", "category", "quantity"]

class CartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItems
        fields = ["productId", "unitPrice", "category", "quantity"]

class UserSerializer(serializers.Serializer):
    class Meta:
        model = User
        fields = ["userId", "userTier", "country", "lifetimeSpend", "ordersPlaced"]

