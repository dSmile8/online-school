from rest_framework import viewsets
from rest_framework.generics import (
    ListAPIView,
    CreateAPIView,
    RetrieveAPIView,
    UpdateAPIView,
    DestroyAPIView, get_object_or_404,
)
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from lms.tasks import send_email_task

from lms.models import Course, Lesson, Subscription
from lms.paginators import LmsPagination
from lms.permissions import IsModerator, IsOwner
from lms.serializers import CourseSerializer, LessonSerializer, SubscriptionSerializer


class CourseViewSet(viewsets.ModelViewSet):
    """ViewSet for Course"""

    serializer_class = CourseSerializer
    queryset = Course.objects.all()
    pagination_class = LmsPagination

    def get_queryset(self):
        if IsModerator().has_permission(self.request, self):
            return Course.objects.all()
        else:
            return Course.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        course = serializer.save()
        course.owner = self.request.user
        send_email_task.delay(course)
        course.save()

    def get_permission(self):
        if self.action in ['update', 'partial_update', 'list', 'retrieve']:
            self.permission_classes = [IsAuthenticated, IsModerator | IsOwner]
        if self.action in 'create':
            self.permission_classes = [IsAuthenticated, ~IsModerator]
        if self.action in 'destroy':
            self.permission_classes = [IsAuthenticated, ~IsModerator | IsOwner]
        return super().get_permissions()


class LessonCreateAPIView(CreateAPIView):
    """Lesson create endpoint"""

    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, ~IsModerator | IsOwner]

    def perform_create(self, serializer):
        lesson = serializer.save()
        lesson.owner = self.request.user
        send_email_task.delay(lesson.course.pk)
        lesson.save()


class LessonListAPIView(ListAPIView):
    """Lesson list endpoint"""

    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated]
    # permission_classes = [AllowAny]
    pagination_class = LmsPagination

    def get_queryset(self):
        if IsModerator().has_permission(self.request, self):
            return Lesson.objects.all()
        else:
            return Lesson.objects.filter(owner=self.request.user)


class LessonRetrieveAPIView(RetrieveAPIView):
    """Lesson retrieve endpoint"""

    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    # permission_classes = [IsAuthenticated, IsModerator | IsOwner]
    permission_classes = [AllowAny]


class LessonUpdateAPIView(UpdateAPIView):
    """Lesson update endpoint"""

    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    # permission_classes = [IsAuthenticated, IsModerator | IsOwner]
    permission_classes = [AllowAny]


class LessonDestroyAPIView(DestroyAPIView):
    """Lesson delete endpoint"""

    queryset = Lesson.objects.all()
    # permission_classes = [IsAuthenticated, ~IsModerator | IsOwner]
    permission_classes = [AllowAny]


class SubscriptionCreateAPIView(CreateAPIView):
    """Subscription create endpoint"""

    serializer_class = SubscriptionSerializer

    def post(self, *args, **kwargs):
        user = self.request.user
        course_id = self.request.data.get('course')
        course_item = get_object_or_404(Course, pk=course_id)

        subscription, created = Subscription.objects.get_or_create(user=user, course=course_item)
        if not created:
            subscription.delete()
            message = 'Subscription was delete'
        else:
            message = 'Subscription added'

        return Response({'message': message})
