from telebot.types import ReplyKeyboardMarkup, KeyboardButton
from ...loader import log


def services():
    """
    Формируем кнопку "Услуги"
    :return:
    """
    log.debug('')
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(KeyboardButton(text="Услуги"))
    log.debug('')
    return keyboard


def confirm_entry():
    """
    Формируем кнопку "Подтвердить запись"
    :return:
    """
    log.debug('')
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(KeyboardButton(text="Подтвердить запись"))
    log.debug('')
    return keyboard
