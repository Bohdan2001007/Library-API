from django.urls import path
from . import views

urlpatterns = [
    path('borrowings/', views.BorrowingList.as_view(), name='borrowing-list-create'),
    path('borrowings/<int:pk>/', views.BorrowingDetail.as_view(), name='borrowing-detail'),
]
