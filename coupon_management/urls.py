"""
URL configuration for coupon_management project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from coupons import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path(
        route='api/',
        view=views.CouponListCreateAPIView.as_view(),
        name='coupon_rest_api'
    ),
    path(
        route='api/<uuid:uuid>/',
        view=views.CouponRetrieveUpdateDestroyAPIView.as_view(),
        name='coupon_rest_api'
    ),
    path(
        route='api/best-coupon/',
        view=views.BestCouponAPIView.as_view(),
        name='best_coupon_api'
    ),
    path(
        route='api/create-user/',
        view=views.CreateUser.as_view(),
        name='create_user_api'
    ),
]
