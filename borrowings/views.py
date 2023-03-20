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
        queryset = Borrowing.objects.filter(clients=user)

        is_active = self.request.query_params.get("is_active")

        if is_active:
            queryset = queryset.filter(is_active=is_active)
        return queryset


class BorrowingDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Borrowing.objects.all()
    serializer_class = BorrowingSerializer
    permission_classes = (IsAuthenticated,)
