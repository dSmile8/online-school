from django.urls import path
from rest_framework.routers import DefaultRouter

from lms.apps import LmsConfig
from lms.views import (
    CourseViewSet,
    LessonCreateAPIView,
    LessonListAPIView,
    LessonUpdateAPIView,
    LessonRetrieveAPIView,
    LessonDestroyAPIView, SubscriptionCreateAPIView,
)

app_name = LmsConfig.name
router = DefaultRouter()

router.register(r"course", CourseViewSet, basename="course")
urlpatterns = [
                  path("lesson/create/", LessonCreateAPIView.as_view(), name="create_lesson"),
                  path("lessons/", LessonListAPIView.as_view(), name="lesson_list"),
                  path("lesson/update/<int:pk>/", LessonUpdateAPIView.as_view(), name="update_lesson"),
                  path("lesson/retrieve/<int:pk>/", LessonRetrieveAPIView.as_view(), name="retrieve_lesson"),
                  path("lesson/destroy/<int:pk>/", LessonDestroyAPIView.as_view(), name="destroy_lesson"),
                  path("subscription/", SubscriptionCreateAPIView.as_view(), name="subscription"),
              ] + router.urls
