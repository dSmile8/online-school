from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from lms.models import Lesson, Course, Subscription
from users.models import User


class LessonTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create(email='test@mail.ru')
        self.course = Course.objects.create(title='test_course', description='test_course_description')
        self.lesson = Lesson.objects.create(title='test_lesson', description='test_lesson_description',
                                            course=self.course)

        self.client.force_authenticate(user=self.user)

    def test_lesson_create(self):
        url = reverse('lms:create_lesson')
        data = {
            'title': 'test_lesson_2',
            'description': 'test_lesson_description_2',
            'course': self.course.pk}
        responce = self.client.post(url, data)
        self.assertEqual(responce.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Lesson.objects.all().count(), 2)

    def test_lesson_update(self):
        url = reverse('lms:update_lesson', args=(self.lesson.pk,))
        data = {
            'title': 'test_lesson_2_2'}

        responce = self.client.patch(url, data)
        self.assertEqual(responce.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get('title'), 'test_lesson_2_2')

    def test_lesson_retrieve(self):
        url = reverse('lms:retrieve_lesson', args=(self.lesson.pk,))
        responce = self.client.get(url)
        self.assertEqual(responce.status_code, status.HTTP_200_OK)

    def test_lesson_delete(self):
        url = reverse('lms:destroy_lesson', args=(self.lesson.pk,))
        responce = self.client.delete(url)
        self.assertEqual(responce.status_code, status.HTTP_204_NO_CONTENT)

    def test_lesson_list(self):
        url = reverse('lms:lesson_list')
        response = self.client.get(url)
        data = response.json()
        result = {'count': 0,
                  'next': None,
                  'previous': None,
                  'results': []}
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data, result)


class SubscriptionTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create(email='test@mail.ru')
        self.course = Course.objects.create(title='test_course', description='test_course_description')
        self.client.force_authenticate(user=self.user)

    def test_subscription_create(self):
        url = reverse('lms:subscription')
        data = {
            'course': self.course.pk
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Subscription.objects.all().count(), 1)
        self.assertEqual(response.json(), {"message": "Subscription added"})

    def test_subscription_delete(self):
        url = reverse('lms:subscription')
        data = {
            'course': self.course.pk
        }
        self.client.post(url, data)
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), {"message": "Subscription was delete"})
        self.assertEqual(Subscription.objects.all().count(), 0)
