from telebot.types import ReplyKeyboardMarkup, KeyboardButton
from ...loader import log


def request_register():
    log.debug('')
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    keyboard.add(KeyboardButton(text="Зарегистрироваться"))
    log.debug('')
    return keyboard


def request_contact():
    log.debug('')
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    keyboard.add(KeyboardButton(text="Отправить номер телефона", request_contact=True))
    log.debug('')
    return keyboard


def request_consent():
    log.debug('')
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    keyboard.add(KeyboardButton(text="Принять"))
    log.debug('')
    return keyboard

