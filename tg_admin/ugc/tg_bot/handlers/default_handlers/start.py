from telebot.types import Message
from ...loader import bot, log, storage
from ...states.states import RegisterStates, ServiceStates
from ...keyboards.reply.reply_requests import request_register, request_contact, request_consent
from ...keyboards.reply.edit_keys import edit_user_data, accept_change
from ...keyboards.reply.function_keys import services
# from ...keyboards.inline.services import services
from ...config_data.config import consent
from ....models import Profile
from ..custom_handlers.get_service import start_service_command


@bot.message_handler(state='*', commands=['start'])
def bot_start(message: Message):
    """
    Запускаем бота, и проверяем зарегистрирован ли пользователь.
    :param message:
    :return:
    """
    log.debug('')
    log.info(f'user_id: {message.from_user.id}, chat_id: {message.chat.id}')
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
        bot.send_message(message.chat.id, f"Здравствуйте, {message.from_user.full_name}! Вы уже зарегистрированы.\n"
                                          f"Теперь вы можете воспользоваться нашими услугами:")
        log.debug('')
        log.info(f'Пользователь уже зарегистрирован: user_id: {message.from_user.id}, chat_id: {message.chat.id}')
        start_service_command(message)


@bot.message_handler(state=RegisterStates.base)
def register(message: Message):
    """
    Запрашиваем согласие на обработку персональных данных.
    :param message:
    :return:
    """
    log.debug('')
    log.info(f'user_id: {message.from_user.id}, chat_id: {message.chat.id}')
    bot.send_message(message.chat.id,
                     consent,
                     reply_markup=request_consent())
    bot.set_state(message.from_user.id, RegisterStates.request_phone, message.chat.id)
    log.debug('')


@bot.message_handler(state=RegisterStates.request_phone)
def request_phone(message: Message):
    """
    Запрашиваем номер телефона
    :param message:
    :return:
    """
    log.debug('')
    log.info(f'user_id: {message.from_user.id}, chat_id: {message.chat.id}')
    bot.set_state(message.from_user.id, RegisterStates.get_user_data, message.chat.id)
    bot.send_message(message.chat.id,
                     "Пожалуйста подтвердите запрос на предоставление доступа к номеру вашего телефона",
                     reply_markup=request_contact())
    log.debug('')


@bot.message_handler(state=RegisterStates.get_user_data, content_types=['contact'])
def get_user_data(message: Message):
    """
    Получаем учетные данные пользователя:

    user_id - id пользователя
    phone - номер телефона пользователя
    first_name - Имя пользователя
    last_name - Фамилия пользователя

    Проверяем корректность учетных данных пользователя
    :param message:
    :return:
    """
    log.debug('')
    log.info(f'user_id: {message.from_user.id}, chat_id: {message.chat.id}')
    with bot.retrieve_data(message.from_user.id, message.chat.id) as user_data:
        user_data['user_id'] = message.from_user.id
        user_data['phone'] = message.contact.phone_number
        user_data['first_name'] = message.contact.first_name
        user_data['last_name'] = message.contact.last_name
    bot.send_message(message.chat.id,
                     f'Ваша учетная запись:\n'
                     f'Имя - {message.from_user.first_name}\n'
                     f'Фамилия - {message.from_user.last_name}',
                     reply_markup=edit_user_data())
    bot.set_state(message.from_user.id, RegisterStates.edit_user_data, message.chat.id)
    log.debug('')


@bot.message_handler(state=RegisterStates.edit_user_data)
def edit_username(message: Message):
    """
    Редактируем учетные данные
    :param message:
    :return:
    """
    log.debug('')
    log.info(f'user_id: {message.from_user.id}, chat_id: {message.chat.id}')
    if message.text == 'Изменить имя':
        log.debug('')
        log.info(f'user_id: {message.from_user.id}, chat_id: {message.chat.id}')
        bot.send_message(message.chat.id, 'Введите новое имя:')
        bot.set_state(message.from_user.id, RegisterStates.edit_first_name, message.chat.id)
        log.debug('')
    elif message.text == 'Изменить фамилию':
        log.debug('')
        log.info(f'user_id: {message.from_user.id}, chat_id: {message.chat.id}')
        bot.send_message(message.chat.id, 'Введите новую фамилию:')
        bot.set_state(message.from_user.id, RegisterStates.edit_last_name, message.chat.id)
        log.debug('')
    elif message.text == 'Завершить редактирование':
        log.debug('')
        log.info(f'user_id: {message.from_user.id}, chat_id: {message.chat.id}')
        with bot.retrieve_data(message.from_user.id, message.chat.id) as user_data:
            try:
                Profile.objects.get_or_create(user_data)
            except Exception as e:
                log.error(e)
        bot.set_state(message.from_user.id, RegisterStates.registered, message.chat.id)
        bot.send_message(
            message.chat.id,
            f'{message.from_user.first_name}, поздравляю! Теперь вы можете воспользоваться нашими услугами',
            reply_markup=services()
        )
        log.debug('')


@bot.message_handler(state=RegisterStates.edit_first_name)
def get_first_name(message: Message):
    """
    Проверяем корректность введенного имени пользователя
    :param message:
    :return:
    """
    log.debug('')
    log.info(f'user_id: {message.from_user.id}, chat_id: {message.chat.id}')
    with bot.retrieve_data(message.from_user.id, message.chat.id) as user_data:
        user_data['first_name'] = message.text
    bot.send_message(message.chat.id, f'Имя - {message.text}', reply_markup=accept_change())
    bot.set_state(message.from_user.id, RegisterStates.new_first_name, message.chat.id)
    log.debug('')


@bot.message_handler(state=RegisterStates.new_first_name)
def apply_first_name(message: Message):
    """
    Запрашиваем подтверждение нового имени
    :param message:
    :return:
    """
    log.debug('')
    log.info(f'user_id: {message.from_user.id}, chat_id: {message.chat.id}')
    if message.text == 'Принять':
        log.debug('')
        bot.set_state(message.from_user.id, RegisterStates.check_user_data, message.chat.id)
        check_user_data(message)
    elif message.text == 'Изменить':
        message.text = 'Изменить имя'
        bot.set_state(message.from_user.id, RegisterStates.edit_user_data, message.chat.id)
        edit_username(message)
    log.debug('')


@bot.message_handler(state=RegisterStates.edit_last_name)
def get_last_name(message: Message):
    """
    Проверяем корректность введенной фамилии пользователя
    :param message:
    :return:
    """
    log.debug('')
    log.info(f'user_id: {message.from_user.id}, chat_id: {message.chat.id}')
    with bot.retrieve_data(message.from_user.id, message.chat.id) as user_data:
        user_data['last_name'] = message.text
    bot.send_message(message.chat.id, f'Фамилия - {message.text}', reply_markup=accept_change())
    bot.set_state(message.from_user.id, RegisterStates.new_last_name, message.chat.id)
    log.debug('')


@bot.message_handler(state=RegisterStates.new_last_name)
def apply_last_name(message: Message):
    """
    Запрашиваем подтверждение новой фамилии
    :param message:
    :return:
    """
    log.debug('')
    log.info(f'user_id: {message.from_user.id}, chat_id: {message.chat.id}')
    if message.text == 'Принять':
        log.debug('')
        bot.set_state(message.from_user.id, RegisterStates.check_user_data, message.chat.id)
        check_user_data(message)
    elif message.text == 'Изменить':
        log.debug('')
        message.text = 'Изменить фамилию'
        bot.set_state(message.from_user.id, RegisterStates.edit_user_data, message.chat.id)
        edit_username(message)
    log.debug('')


@bot.message_handler(state=RegisterStates.check_user_data)
def check_user_data(message: Message):
    """
    Проверяем корректность учетных данных пользователя
    :param message:
    :return:
    """
    log.debug('')
    log.info(f'user_id: {message.from_user.id}, chat_id: {message.chat.id}')
    with bot.retrieve_data(message.from_user.id, message.chat.id) as user_data:
        log.debug('')
        bot.send_message(message.chat.id,
                         f'Ваша учетная запись:\n'
                         f'Имя - {user_data["first_name"]}\n'
                         f'Фамилия - {user_data["last_name"]}',
                         reply_markup=edit_user_data())
    bot.set_state(message.from_user.id, RegisterStates.edit_user_data, message.chat.id)
    log.debug('')
