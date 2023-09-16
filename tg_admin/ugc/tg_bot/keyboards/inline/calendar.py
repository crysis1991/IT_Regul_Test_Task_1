import calendar
import locale
from datetime import datetime
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup
from ...loader import log


def create_calendar_callback_data(action, year, month, day, state):
    """ Создает callback data для каждой кнопки"""
    log.debug('')
    data = ','.join([action, str(year), str(month), str(day), state])
    return data


def separate_calendar_callback_data(data):
    """ Разбирает callback_data """
    log.debug('')
    return data.split(',')


def create_calendar(year=None, month=None, state=None):
    """
    Создает календарь с указанным годом и месяцем
    :param state:
    :param int year: Год используемый при создании календаря, если None то используется текущий год.
    :param int month: Месяц используемый при создании календаря, если None то используется текущий месяц.
    :return: Возвращает объект InlineKeyboardMarkup с календарем.
    """
    log.debug('')
    locale.setlocale(category=locale.LC_ALL, locale='Russian')
    now = datetime.now()
    year = now.year if year is None else year
    month = now.month if month is None else month
    my_calendar = calendar.monthcalendar(year, month)
    week_days = ["Пн", "Вт", "Ср", "Чт", "Пт", "Сб", "Вс"]
    data_ignore = create_calendar_callback_data("IGNORE", year, month, 0, state)
    keyboard = InlineKeyboardMarkup()
    log.debug('')
    keyboard.add(InlineKeyboardButton(' '.join([calendar.month_name[month], str(year)]), callback_data=data_ignore))
    log.debug('')
    keyboard.add(*[InlineKeyboardButton(day, callback_data=data_ignore) for day in week_days], row_width=7)
    log.debug('')
    for week in my_calendar:
        row = []
        for day in week:
            if day == 0:
                log.debug('')
                row.append(InlineKeyboardButton(text=' ', callback_data=data_ignore))
            elif month <= now.month and day < now.day:
                row.append(
                    InlineKeyboardButton(str(day),
                                         callback_data=create_calendar_callback_data("IGNORE", year, month, day,
                                                                                     state)))
            else:
                log.debug('')
                row.append(
                    InlineKeyboardButton(str(day),
                                         callback_data=create_calendar_callback_data("DAY", year, month, day, state)))
        log.debug('')
        keyboard.add(*row, row_width=7)
    log.debug('')
    null_key = InlineKeyboardButton(" ",
                                    callback_data=create_calendar_callback_data("IGNORE", year, month, 0, state))
    prev_month = InlineKeyboardButton("<",
                                      callback_data=create_calendar_callback_data("PREV-MONTH", year, month, 0, state))
    back = InlineKeyboardButton("Назад", callback_data=create_calendar_callback_data("BACK", year, month, 0, state))
    next_month = InlineKeyboardButton(">",
                                      callback_data=create_calendar_callback_data("NEXT-MONTH", year, month, 0, state))
    if month <= now.month:
        log.debug('')
        keyboard.add(null_key, back, next_month)
    else:
        log.debug('')
        keyboard.add(prev_month, back, next_month)
    log.debug('')
    return keyboard
