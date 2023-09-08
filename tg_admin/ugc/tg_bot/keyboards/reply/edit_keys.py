from telebot.types import ReplyKeyboardMarkup, KeyboardButton
from ...loader import log


def edit_user_data():
    """
    Формируем кнопки редактирования учетных данных пользователя
    :return:
    """
    log.debug('')
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    keyboard.row(
        KeyboardButton(text="Изменить имя"),
        KeyboardButton(text="Изменить фамилию")
    )
    keyboard.row(KeyboardButton(text="Завершить редактирование"))
    log.debug('')
    return keyboard


def accept_change():
    """
    Формируем кнопки Принять и Изменить для редактирования учетных данных пользователя'
    :return:
    """
    log.debug('')
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    keyboard.add(
        KeyboardButton("Принять"),
        KeyboardButton("Изменить")
    )
    log.debug('')
    return keyboard
