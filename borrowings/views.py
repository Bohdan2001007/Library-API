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
        """
        This view should return a list of all the borrowings
        for the currently authenticated user.
        """
        user = self.request.user
        return Borrowing.objects.filter(client=user)


class BorrowingDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Borrowing.objects.all()
    serializer_class = BorrowingSerializer
    permission_classes = (IsAuthenticated,)
