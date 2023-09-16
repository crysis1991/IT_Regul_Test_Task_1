from django.db import models
from datetime import date


class Profile(models.Model):
    """
    Модель таблицы пользователя.
    """
    user_id = models.PositiveIntegerField(
        verbose_name='ID пользователя Telegram',
        unique=True
    )
    phone = models.TextField(
        verbose_name='Номер телефона пользователя',
        unique=True
    )
    first_name = models.TextField(
        verbose_name='Имя пользователя'
    )
    last_name = models.TextField(
        verbose_name='Фамилия пользователя'
    )

    def __str__(self):
        return f'{self.user_id} {self.first_name} {self.last_name}'

    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'


class Service(models.Model):
    """
    Модель таблицы услуг
    """
    page = models.IntegerField(
        primary_key=True,
        verbose_name='Страница'
    )
    title = models.TextField(
        verbose_name='Услуга'
    )
    description = models.TextField(
        verbose_name='Описание услуги'
    )

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = 'Услуга'
        verbose_name_plural = 'Услуги'


class SubService(models.Model):
    """
    Модель таблицы под услуг
    """
    page = models.IntegerField(
        verbose_name='Страница'
    )
    title = models.TextField(
        verbose_name='Услуга'
    )
    description = models.TextField(
        verbose_name='Описание услуги'
    )
    service = models.ForeignKey(
        Service,
        on_delete=models.PROTECT,
        verbose_name='Родительская услуга'
    )
    price = models.DecimalField(default=0, max_digits=8, decimal_places=2)

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = 'Подуслуга'
        verbose_name_plural = 'Подуслуги'


class Date(models.Model):
    date = models.DateField(verbose_name='Дата', unique=True)

    def __str__(self):
        return f'{self.date}'

    class Meta:
        verbose_name = 'Дата'
        verbose_name_plural = 'Дата'


class TimeSlot(models.Model):
    """
    Модель таблицы слотов времени для услуги
    """
    time = models.TimeField(verbose_name='Время', unique=True)

    def __str__(self):
        return f'{self.time}'

    class Meta:
        verbose_name = 'Слот времени'
        verbose_name_plural = 'Слоты времени'


class Order(models.Model):
    """
        Модель таблицы записей на получение услуг
        """
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(Profile, on_delete=models.PROTECT, verbose_name='Пользователь')
    service = models.ForeignKey(SubService, on_delete=models.PROTECT, verbose_name='Услуга')
    date = models.ForeignKey(Date, on_delete=models.PROTECT, verbose_name='Дата')
    time = models.ForeignKey(TimeSlot, on_delete=models.PROTECT, verbose_name='Время')

    class Meta:
        verbose_name = 'Запись'
        verbose_name_plural = 'Записи'
