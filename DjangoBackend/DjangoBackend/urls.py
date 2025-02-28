from django.contrib import admin
from django.urls import path, include
from rest_framework import routers

from products.views import ProductViewSet, UserViewSet  # Import UserViewSet instead of UserAPIView

# Create a single router and register both viewsets
router = routers.DefaultRouter()
router.register('products', ProductViewSet)
router.register('users', UserViewSet)  # Now using UserViewSet instead of UserAPIView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),  # This includes both /api/products/ and /api/users/
]
