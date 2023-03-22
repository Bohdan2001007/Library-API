from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from .models import Borrowing
from .serializers import BorrowingSerializer, BorrowingCreateSerializer


class BorrowingList(generics.ListCreateAPIView):
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
    queryset = Borrowing.objects.all()
    serializer_class = BorrowingSerializer
    permission_classes = (IsAuthenticated,)
