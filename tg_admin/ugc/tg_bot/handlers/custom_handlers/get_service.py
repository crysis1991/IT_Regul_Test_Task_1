from telebot.types import Message, CallbackQuery
from datetime import datetime, timedelta, date, time
from ...loader import bot, log
from ...states.states import RegisterStates, ServiceStates
from ....models import Profile, SubService, Order, Date, TimeSlot
from ...keyboards.inline.services import get_service_button, separate_service_callback_data
from ...keyboards.inline.calendar import create_calendar, separate_calendar_callback_data
from ...keyboards.inline.time_slots import create_time_slots, separate_time_slots_callback_data
from ...keyboards.reply.function_keys import confirm_entry
from ...keyboards.reply.reply_requests import request_register


@bot.callback_query_handler(func=lambda call: call.data.split(',')[-1] == 'RegisterStates.registered')
def get_service(call: CallbackQuery):
    log.debug('')
    log.info(f'user_id: {call.from_user.id}, chat_id: {call.message.chat.id}')
    start_service_command(call.message)
    bot.answer_callback_query(callback_query_id=call.id)
    log.debug('')


@bot.message_handler(func=lambda message: message.text == 'Услуги', state=RegisterStates.registered)
def reply_get_service(message: Message):
    log.debug('')
    start_service_command(message)


@bot.message_handler(state='*', commands=['services'])
def start_service_command(message: Message):
    """
    Выводим список услуг
    :param message:
    :return:
    """
    log.debug('')
    bot.set_state(message.from_user.id, ServiceStates.base, message.chat.id)
    log.debug('')
    if Profile.objects.filter(user_id=message.from_user.id).first() is None:
        log.debug('')
        log.info(f'Новый пользователь: user_id: {message.from_user.id}, chat_id: {message.chat.id}')
        bot.send_message(message.chat.id,
                         f"Здравствуйте, {message.from_user.full_name}! "
                         f"Для продолжения работы необходимо зарегистрироваться",
                         reply_markup=request_register()
                         )
        bot.set_state(message.from_user.id, RegisterStates.base, message.chat.id)
        log.debug('')
    else:
        log.debug('')
        bot.send_message(
            message.chat.id,
            text='Выберите услугу',
            reply_markup=get_service_button(state='ServiceStates.base')
        )
    log.debug('')


@bot.callback_query_handler(func=lambda call: call.data.split(',')[-1] == 'ServiceStates.base')
def scroll_service(call: CallbackQuery):
    log.debug('')
    log.info(f'user_id: {call.from_user.id}, chat_id: {call.message.chat.id}')
    action, page, level, service_id, state = separate_service_callback_data(call.data)
    if action == 'to':
        log.debug('')

        bot.edit_message_text(
            text=call.message.text,
            chat_id=call.message.chat.id,
            message_id=call.message.id,
            reply_markup=get_service_button(page=int(page), level=int(level), service_id=service_id,
                                            state='ServiceStates.base')
        )
    elif action == 'select service':
        log.debug('')
        # with bot.retrieve_data(call.from_user.id, call.message.chat.id) as data:
        #     data['service'] = page
        bot.edit_message_text(
            text=call.message.text,
            chat_id=call.message.chat.id,
            message_id=call.message.id,
            reply_markup=get_service_button(service_id=service_id, level=level, state='ServiceStates.base')
        )
    elif action == 'IGNORE':
        log.debug('')
        bot.answer_callback_query(callback_query_id=call.id)
    else:
        log.debug('')
        with bot.retrieve_data(call.from_user.id, call.message.chat.id) as data:
            data['user'] = Profile.objects.get(user_id=call.from_user.id)
            data['service'] = SubService.objects.get(title=service_id)
        log.debug('')
        bot.edit_message_text(text=call.message.text,
                              chat_id=call.message.chat.id,
                              message_id=call.message.id
                              )
        bot.answer_callback_query(callback_query_id=call.id)
        bot.delete_message(call.message.chat.id, call.message.id)
        bot.set_state(call.from_user.id, ServiceStates.sub_service, call.message.chat.id)
        get_date(call.message)
        log.debug('')


@bot.message_handler(state=ServiceStates.sub_service)
def get_date(message: Message):
    log.debug('')
    log.info(f'user_id: {message.from_user.id}, chat_id: {message.chat.id}')
    bot.send_message(
        message.chat.id,
        'Выберите дату приема:',
        reply_markup=create_calendar(state='ServiceStates.sub_service')
    )
    bot.set_state(message.from_user.id, ServiceStates.date, message.chat.id)
    log.debug('')


@bot.callback_query_handler(func=lambda call: call.data.split(',')[-1] == 'ServiceStates.sub_service')
def process_calendar_selection(call: CallbackQuery):
    """
    Обработка callback_query. ЭЭтот метод генерирует новый календарь при нажатии кнопки "Вперед" или
    "назад". Этот метод должен вызываться внутри обработчика запроса обратного вызова.
    :param call:
    :return: Returns a tuple (Boolean,datetime.datetime), indicating if a date is selected
                and returning the date if so.
    """
    log.debug('')
    log.info(f'user_id: {call.from_user.id}, chat_id: {call.message.chat.id}')
    (action, year, month, day, state) = separate_calendar_callback_data(call.data)
    curr = datetime(int(year), int(month), 1)
    if action == "IGNORE":
        log.debug('')
        bot.answer_callback_query(callback_query_id=call.id)
    elif action == "DAY":
        log.debug('')
        bot.edit_message_text(text=call.message.text,
                              chat_id=call.message.chat.id,
                              message_id=call.message.id
                              )
        if Date.objects.filter(date=date(int(year), int(month), int(day))).first() is None:
            Date.objects.create(date=date(int(year), int(month), int(day)))
        with bot.retrieve_data(call.from_user.id, call.message.chat.id) as data:
            data['date'] = Date.objects.get(date=date(int(year), int(month), int(day)))
        bot.answer_callback_query(callback_query_id=call.id)
        bot.set_state(call.from_user.id, ServiceStates.date, call.message.chat.id)
        get_time(call.message)
    elif action == "PREV-MONTH":
        log.debug('')
        pre = curr - timedelta(days=1)
        bot.edit_message_text(text=call.message.text,
                              chat_id=call.message.chat.id,
                              message_id=call.message.id,
                              reply_markup=create_calendar(int(pre.year), int(pre.month), state=state))
    elif action == "NEXT-MONTH":
        log.debug('')
        ne = curr + timedelta(days=31)
        bot.edit_message_text(text=call.message.text,
                              chat_id=call.message.chat.id,
                              message_id=call.message.id,
                              reply_markup=create_calendar(int(ne.year), int(ne.month), state=state))
    elif action == "BACK":
        log.debug('')
        bot.delete_message(call.message.chat.id, call.message.id)
        start_service_command(call.message)
    else:
        log.error('Something went wrong!')
        bot.answer_callback_query(callback_query_id=call.id, text="Что-то пошло не так!")


@bot.message_handler(state=ServiceStates.date)
def get_time(message: Message):
    log.debug('')
    log.info(f'user_id: {message.from_user.id}, chat_id: {message.chat.id}')
    bot.send_message(
        message.chat.id,
        'Выберите время приема:',
        reply_markup=create_time_slots(state='ServiceStates.date')
    )

    bot.delete_message(message.chat.id, message.id)
    bot.set_state(message.from_user.id, ServiceStates.time, message.chat.id)
    log.debug('')
    log.debug('')


@bot.callback_query_handler(func=lambda call: call.data.split(',')[-1] == 'ServiceStates.date')
def select_time(call: CallbackQuery):
    log.debug('')
    log.info(f'user_id: {call.from_user.id}, chat_id: {call.message.chat.id}')
    action, state = separate_time_slots_callback_data(call.data)
    if action == "BACK":
        log.debug('')
        bot.delete_message(call.message.chat.id, call.message.id)
        get_date(call.message)
    else:
        log.debug('')
        bot.set_state(call.from_user.id, ServiceStates.time, call.message.chat.id)
        hour, minute = action.split(':')
        if TimeSlot.objects.filter(time=time(int(hour), int(minute))).first() is None:
            TimeSlot.objects.create(time=time(int(hour), int(minute)))
        with bot.retrieve_data(call.from_user.id, call.message.chat.id) as data:
            data['time'] = TimeSlot.objects.get(time=time(int(hour), int(minute)))
        bot.send_message(call.message.chat.id,
                         f'Подтвердите запись:\n'
                         f'Услуга - {data["service"]}\n'
                         f'Дата - {data["date"]}\n'
                         f'Время - {data["time"]}\n'
                         f'Стоимость: 500 р',
                         reply_markup=confirm_entry())
        bot.answer_callback_query(callback_query_id=call.id)
        log.debug('')


@bot.message_handler(state=ServiceStates.time)
def get_entry(message: Message):
    """
    Подтверждаем запись и возвращаемся к списку услуг
    :param message:
    :return:
    """
    log.debug('')
    log.info(f'user_id: {message.from_user.id}, chat_id: {message.chat.id}')
    if message.text == 'Подтвердить запись':
        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            print(data)
            Order.objects.get_or_create(data)
        log.debug('')
        bot.set_state(message.from_user.id, RegisterStates.registered, message.chat.id)
        start_service_command(message)
