from telebot.handler_backends import State, StatesGroup
from telebot import custom_filters
from ..loader import log, bot


class UserStates(StatesGroup):
    log.debug('')
    base = State()
    request_phone = State()
    get_user_data = State()
    check_user_data = State()
    edit_first_name = State()
    edit_last_name = State()
    new_first_name = State()
    new_last_name = State()
    edit_user_data = State()


bot.add_custom_filter(custom_filters.StateFilter(bot))
