from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from .models import Borrowing
from .serializers import BorrowingSerializer, BorrowingCreateSerializer


class BorrowingList(generics.ListCreateAPIView):
    """
        List all borrowing records or create a new borrowing record.

        - Authenticated users can view their own borrowing records.
        - Staff users can view the borrowing records of a specific user by providing a user_id in the query parameters.
        - The is_active query parameter can be used to filter borrowing records based on their active status.
        - To create a new borrowing record, provide book_id and expected_return_date.
    """
    queryset = Borrowing.objects.all()
    serializer_class = BorrowingSerializer
    permission_classes = (IsAuthenticated,)

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return BorrowingCreateSerializer
        return BorrowingSerializer

    def get_queryset(self):
        user = self.request.user
        queryset = Borrowing.objects.filter(client=user)

        is_active = self.request.query_params.get("is_active")

        if is_active:
            queryset = queryset.filter(is_active=is_active)

        user_id = self.request.query_params.get("user_id")

        if user.is_staff and user_id:
            queryset = queryset.filter(client=user_id)
        else:
            queryset = queryset.filter(client=user)

        return queryset


class BorrowingDetail(generics.RetrieveUpdateDestroyAPIView):
    """
        Retrieve, update or delete a borrowing record.

        - Authenticated users can view, update, or delete their own borrowing records.
        - Staff users can view, update, or delete any borrowing record.
    """
    queryset = Borrowing.objects.all()
    serializer_class = BorrowingSerializer
    permission_classes = (IsAuthenticated,)
