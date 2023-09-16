from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from ...loader import log
from ....models import Service, SubService


def create_service_callback_data(action='None', page='1', level='1', service_id='None', state='None'):
    """ Создает callback data для каждой кнопки"""
    log.debug('')
    data = ','.join([action, page, level, service_id, state])
    return data


def separate_service_callback_data(data):
    """ Разбирает callback_data """
    log.debug('')
    return data.split(',')


def services():
    log.debug('')
    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton(
        'Услуги',
        callback_data=create_service_callback_data(action='services', state='RegisterStates.registered'))
    )
    log.debug('')
    return keyboard


def get_service_button(service_id: int = None, level: int = 1, state: str = 'ServiceStates.base', pages_count: int = 1,
                       page: int = 1):
    log.debug('')
    if level == 1:
        log.debug('')
        all_services = Service.objects.all()
        pages_count = len(all_services)
        service = all_services.filter(page=page).values_list('title', 'description')
    else:
        log.debug('')
        all_services = SubService.objects.select_related('service').filter(service_id=service_id)
        pages_count = len(all_services)
        service = all_services.filter(page=page).values_list('title', 'description')
    log.debug('')
    keyboard = InlineKeyboardMarkup()
    left = page - 1 if page != 1 else 1
    right = page + 1 if page != pages_count else pages_count
    log.debug('')
    data_ignore = create_service_callback_data(action="IGNORE", page=str(page), level=str(level),
                                               service_id=str(service_id), state=state)
    log.debug('')
    keyboard.add(InlineKeyboardButton(text=f"Название: *{service[0][0]}*", callback_data=data_ignore))
    keyboard.add(InlineKeyboardButton(text=f"Описание: *{service[0][1]}*", callback_data=data_ignore))
    log.debug('')
    keyboard.add(
        *[InlineKeyboardButton(text="←",
                               callback_data=create_service_callback_data(action='to', page=str(left), level=str(level),
                                                                          service_id=str(service_id), state=state)),
          InlineKeyboardButton(text=f"{str(page)}/{str(pages_count)}", callback_data=data_ignore),
          InlineKeyboardButton(text="→",
                               callback_data=create_service_callback_data(action='to', page=str(right),
                                                                          level=str(level),
                                                                          service_id=str(service_id), state=state))])

    if level == 1:
        log.debug('')
        select_button = InlineKeyboardButton(text="ВЫБРАТЬ", callback_data=create_service_callback_data(
            action='select service',
            page=str(page),
            level=str(level + 1),
            service_id=str(page),
            state=state
        )
                                             )
        log.debug('')
        keyboard.add(select_button)
    else:
        log.debug('')

        select_button = InlineKeyboardButton(text="ВЫБРАТЬ", callback_data=create_service_callback_data(
            action='select sub_service',
            page=str(page),
            service_id=service[0][0],
            state=state
        )

                                             )
        log.debug('')
        keyboard.add(select_button)
    log.debug('')
    return keyboard
