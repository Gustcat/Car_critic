from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator


User = get_user_model()


class Country(models.Model):
    name = models.CharField(
        max_length=25,
        unique=True,
        verbose_name='Название страны'
    )

    class Meta:
        verbose_name = 'Страна'
        verbose_name_plural = 'Страны'

    def __str__(self):
        return self.name


class Producer(models.Model):
    name = models.CharField(
        max_length=25,
        unique=True,
        verbose_name='Наименование производителя'
    )
    country = models.ForeignKey(
        Country,
        related_name='producers',
        on_delete=models.CASCADE,
        verbose_name='Страна'
    )

    class Meta:
        verbose_name = 'Производитель'
        verbose_name_plural = 'Производители'

    def __str__(self):
        return self.name


class Car(models.Model):
    name = models.CharField(
        max_length=25,
        unique=True,
        verbose_name='Название автомобиля'
    )
    producer = models.ForeignKey(
        Producer,
        on_delete=models.CASCADE,
        related_name='cars',
        verbose_name='Производитель'
    )
    inception_year = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1900),
                    MaxValueValidator(2100)],
        verbose_name='Год начала выпуска',
    )
    completion_year = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1900),
                    MaxValueValidator(2100)],
        blank=True,
        null=True,
        verbose_name='Год окончания выпуска',
    )

    class Meta:
        verbose_name = 'Автомобиль'
        verbose_name_plural = 'Автомобили'

    def __str__(self):
        return self.name


class Comment(models.Model):
    email = models.EmailField(
        max_length=25,
        verbose_name='Электронная почта',
    )
    car = models.ForeignKey(
        Car,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Автомобиль'
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        editable=False,
        verbose_name='Дата создания')
    comment = models.TextField(
        verbose_name='Комментарий'
    )

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return f'{self.email}: {self.comment[:25]}'
