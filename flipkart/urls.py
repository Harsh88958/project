from django.contrib import admin
from django.urls import path, include

from . import views
from rest_framework import routers
from .views import UserViewSet

router = routers.DefaultRouter()
router.register(r"", UserViewSet)

urlpatterns = [
    path("", views.index, name="home"),
    path("signup", views.signup, name="sign"),
    path("login", views.login, name="login"),
    path("logout", views.logout, name="logout"),
    path("cart/", views.cart_details, name="cart"),
    path("checkout", views.checkout, name="checkout"),
    path("order", views.order, name="order"),
    path("rest/", include(router.urls)),
    path("api-auth/", include("rest_framework.urls", namespace="rest_framework")),
]
