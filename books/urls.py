from django.urls import path, include
from rest_framework import routers
from .views import BookViewSet

router = routers.DefaultRouter()
router.register(r'books', BookViewSet)

app_name = "books"

urlpatterns = [
    path('', include(router.urls)),
    path('books/<int:pk>/', BookViewSet.as_view({'get': 'retrieve'}), name='book-detail-api'),
]
