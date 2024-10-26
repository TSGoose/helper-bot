import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
import requests

# Токен вашего сообщества
VK_TOKEN = 'vk1.a.PPA1xA0JtOT3Q1YG4vF57wZ763XRnNkzOKppKgWY4Hy-xGdm8nyuv_lLZwY8cxZ2gUPvgw50YHHvOcETf5ykvr4dFzWkDRRUm8ChJt0PlWeFIbuQQMMCqxXnTwHP3S_gVpkK0SVKokrkIy2P0m-g61fWtMbUnOkPCYlN75gRjAxNm3JIiCEVJosV1ZsN9kwzBcI6PtAo151XkR8orr4SHQ'

# URL стороннего API
API_URL = 'https://api.example.com/data'  # Замените на реальный URL API

# Инициализация сессии ВКонтакте
vk_session = vk_api.VkApi(token=VK_TOKEN)
vk = vk_session.get_api()
longpoll = VkLongPoll(vk_session)

# Функция для отправки запроса на сторонний API
def call_external_api(user_message):
    try:
        response = requests.get(API_URL, params={'message': user_message})
        if response.status_code == 200:
            data = response.json()
            return data.get('answer', 'Нет данных в ответе')
        else:
            return f"Ошибка API: {response.status_code}"
    except requests.RequestException as e:
        return f"Произошла ошибка при запросе: {e}"

# Функция для отправки сообщения пользователю
def send_message(user_id, message):
    vk.messages.send(
        user_id=user_id,
        message=message,
        random_id=0  # random_id для предотвращения дублирования сообщений
    )

# Основной цикл бота
for event in longpoll.listen():
    # Если получено сообщение
    if event.type == VkEventType.MESSAGE_NEW and event.to_me:
        user_message = event.text  # Получаем текст сообщения от пользователя
        user_id = event.user_id  # Получаем ID пользователя

        # Отправляем сообщение на сторонний API и получаем ответ
        api_response = call_external_api(user_message)

        # Отправляем ответ пользователю
        send_message(user_id, api_response)
