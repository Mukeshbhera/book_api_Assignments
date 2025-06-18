# from django.urls import path
from . import views

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BookViewSet

router = DefaultRouter()
router.register(r'books', BookViewSet)

urlpatterns = [
    path('protected/', views.protected_view, name='protected_view'),
    path('api/', include(router.urls)),
    path('', include(router.urls)),
]
