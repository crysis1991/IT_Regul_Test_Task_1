from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup
from ...loader import log


def create_time_slots_callback_data(my_time, state):
    """ Создает callback data для каждой кнопки"""
    log.debug('')
    data = ','.join([my_time, state])
    return data


def separate_time_slots_callback_data(data):
    """ Разбирает callback_data """
    log.debug('')
    return data.split(',')


def create_time_slots(state):
    """
    Создает сетку с тайм-слотами
    :param state:
    :return: Возвращает объект InlineKeyboardMarkup с тайм-слотами.
    """
    log.debug('')
    keyboard = InlineKeyboardMarkup()
    time_slots = ['08:00', '08:30', '09:00', '09:30', '10:00', '10:30', '11:00', '11:30', '13:00', '13:30', '14:00',
                  '14:30', '15:00', '15:30', '16:00', '16:30']
    data_ignore = create_time_slots_callback_data("IGNORE", state)
    keyboard.add(*[InlineKeyboardButton(text=i,
                                        callback_data=create_time_slots_callback_data(i, state=state)) for i in
                   time_slots], row_width=4)
    keyboard.add(InlineKeyboardButton(text='Назад', callback_data=create_time_slots_callback_data('BACK', state)))
    return keyboard
