from django.contrib.auth.models import AbstractUser
from django.db import models

from lms.models import Course, Lesson

NULLABLE = {"blank": True, "null": True}


class User(AbstractUser):
    name = None
    email = models.EmailField(unique=True, verbose_name="почта")
    phone = models.CharField(max_length=30, verbose_name="телефон", **NULLABLE)
    city = models.CharField(max_length=50, verbose_name="город", **NULLABLE)
    image = models.ImageField(upload_to="user", verbose_name="изображение", **NULLABLE)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = "пользователь"
        verbose_name_plural = "пользователи"


class Payment(models.Model):
    user = models.ForeignKey(User, verbose_name="пользователь", on_delete=models.CASCADE)
    course = models.ForeignKey(Course, verbose_name="курс", on_delete=models.CASCADE, **NULLABLE)
    lesson = models.ForeignKey(Lesson, verbose_name='лекция', on_delete=models.CASCADE, **NULLABLE)
    payment_date = models.DateTimeField(auto_now_add=True, verbose_name="дата оплаты")
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="сумма оплаты")
    payment_status = models.CharField(max_length=50, verbose_name="статус оплаты")
    payment_method = models.CharField(max_length=50, verbose_name="тип оплаты")

    def __str__(self):
        return f"{self.user} - {self.course} - {self.lesson} - {self.payment_status}"

    class Meta:
        verbose_name = "платеж"
        verbose_name_plural = "платежи"
