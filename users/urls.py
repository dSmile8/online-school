from django.urls import path
from rest_framework.routers import DefaultRouter
from users.views import UsersViewSet, PaymentListAPIView

from users.apps import UsersConfig

app_name = UsersConfig.name
router = DefaultRouter()

router.register(r"user", UsersViewSet, basename="user")

urlpatterns = [
                path('payments/', PaymentListAPIView.as_view(), name='payments')
              ] + router.urls
