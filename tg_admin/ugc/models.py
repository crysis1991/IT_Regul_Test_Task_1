from django.db import models


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
        return f'#{self.user_id} {self.first_name} {self.last_name}'

    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'
