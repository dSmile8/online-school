from django.db import models

from config import settings

NULLABLE = {"blank": True, "null": True}


class Course(models.Model):
    title = models.CharField(max_length=150, verbose_name="название")
    image = models.ImageField(upload_to="course", verbose_name="изображение", **NULLABLE)
    description = models.TextField(verbose_name="описание")
    owner = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='владелец',
                              **NULLABLE)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "курс"
        verbose_name_plural = "курсы"


class Lesson(models.Model):
    title = models.CharField(max_length=150, verbose_name="название")
    description = models.TextField(verbose_name="описание")
    image = models.ImageField(upload_to="lesson", verbose_name="изображение", **NULLABLE)
    url = models.URLField(verbose_name="ссылка на видео", **NULLABLE)
    course = models.ForeignKey(Course, verbose_name="курсы", on_delete=models.CASCADE)
    owner = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='владелец',
                              **NULLABLE)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "урок"
        verbose_name_plural = "уроки"


class Subscription(models.Model):
    user = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Пользователь',
                             **NULLABLE)
    course = models.ForeignKey(to=Course, verbose_name="Курс", on_delete=models.CASCADE, **NULLABLE)

    def __str__(self):
        return f"{self.user} - {self.course}"

    class Meta:
        verbose_name = "Подписка"
        verbose_name_plural = "Подписки"