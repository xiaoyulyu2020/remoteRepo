
from django.contrib import admin
from django.urls import path
from rest_framework import routers

from products.views import ProductViewSet

router = routers.DefaultRouter()
router.register('products', ProductViewSet)
urlpatterns = [
    path('admin/', admin.site.urls),
]
