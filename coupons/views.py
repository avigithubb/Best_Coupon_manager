from urllib import request
from django.shortcuts import render
from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView
)
from django.http import HttpRequest
from rest_framework.permissions import IsAuthenticated
from .models import Coupons, User, CartItems
from .api.serializers import CouponSerializer, UserSerializer, CartItemSerializer
import time

# Create your views here.

class CouponListCreateAPIView(ListCreateAPIView):
    queryset = Coupons.objects.all()
    permission_classes = (IsAuthenticated, )
    serializer_class = CouponSerializer
    lookup_field = 'uuid'

    def get_queryset(self):
        queryset = super().get_queryset()
        data = self.request.data
        user_id = data.get('userId', None)

        user_tier = User.objects.get(id=user_id).userTier

        coupons = Coupons.objects.filter(
            eligibility__icontains=user_tier,
            startDate__lte =  time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime()),
            endDate__gte = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime())
        )

        return coupons

class CouponRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Coupons.objects.all()
    permission_classes = (IsAuthenticated, )
    serializer_class = CouponSerializer
    lookup_field = 'uuid'

class BestCouponAPIView(ListCreateAPIView):
    queryset = Coupons.objects.all()
    serializer_class = CouponSerializer

    def get_queryset(self):
        data = self.request.data
        user_id = data.get('userId', None)
        cart_items_data = data.get('cartItems', [])

        user = User.objects.get(id=user_id)
        cart_items = []
        for item_data in cart_items_data:
            cart_item = CartItems(
                productId=item_data['productId'],
                unitPrice=item_data['unitPrice'],
                category=item_data['category'],
                quantity=item_data.get('quantity', 1),
                user=user
            )
            cart_items.append(cart_item)

        # Logic to determine the best coupon based on cart items and user details
        # This is a placeholder for the actual implementation
        best_coupon = None
        best_discount = 0

        for coupon in Coupons.objects.all():
            total_discount = 0
            for item in cart_items:
                if coupon.discountType == 'percentage':
                    discount = (coupon.discountValue / 100) * item.unitPrice * item.quantity
                elif coupon.discountType == 'fixed':
                    discount = coupon.discountValue * item.quantity
                else:
                    discount = 0

                if coupon.maxDiscountAmount and discount > coupon.maxDiscountAmount:
                    discount = coupon.maxDiscountAmount

                total_discount += discount

            if total_discount > best_discount:
                best_discount = total_discount
                best_coupon = coupon

        if best_coupon:
            return Coupons.objects.filter(id=best_coupon.id)
        else:
            return Coupons.objects.none()

class CreateUser(ListCreateAPIView):
    queryset = Coupons.objects.all()
    serializer_class = UserSerializer

    def get_queryset(self):
        return User.objects.all()
    
    def create_user(self, request: HttpRequest):
        user = User.objects.create(
            userTier=request.data.get('userTier'),
            country=request.data.get('country'),
            lifetimeSpend=request.data.get('lifetimeSpend', 0.00),
            ordersPlaced=request.data.get('ordersPlaced', 0)
        )
        user.save()
        return user


class CreateCartItem(ListCreateAPIView):
    queryset = CartItems.objects.all()
    serializer_class = CartItemSerializer
    Permission_classes = (IsAuthenticated, )

    def get_queryset(self):
        return CartItems.objects.all()
    
    def create_cart_item(self, request: HttpRequest):
        user = User.objects.get(id=request.data.get('userId'))
        cart_item = CartItems.objects.create(
            productId=request.data.get('productId'),
            unitPrice=request.data.get('unitPrice'),
            category=request.data.get('category'),
            quantity=request.data.get('quantity', 1),
            user=user
        )
        cart_item.save()
        return cart_item
