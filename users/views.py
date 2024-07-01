from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.generics import ListAPIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import OrderingFilter

from users.models import User, Payment
from users.serializers import UsersSerializer, PaymentSerializer


class UsersViewSet(ModelViewSet):
    serializer_class = UsersSerializer
    queryset = User.objects.all()


class PaymentListAPIView(ListAPIView):
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = '__all__'
    ordering_fields = ('amount', 'payment_date',)
