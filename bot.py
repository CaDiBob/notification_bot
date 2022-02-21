import logging
import requests
import telegram
import time

from environs import Env


logger = logging.getLogger('bot')


def send_notifications(bot, answer, chat_id):
    for result  in answer.get('new_attempts'):
        lesson_title = result.get('lesson_title')
        lesson_url = result.get('lesson_url')
        result = result.get('is_negative')
        if result:
            bot.send_message(
                text=f'''Преподаватель проверил работу "{lesson_title}"
                \nЕсть ошибки, работа не принята.
                \nссылка: {lesson_url}''',
                chat_id=chat_id,
            )
        else:
            bot.send_message(
                text=f'''Преподаватель проверил работу "{lesson_title}"
                \nОшибок нет, работа принята
                \nссылка {lesson_url}''',
                chat_id=chat_id,
            )


def make_requests(headers, bot, chat_id):
    url = 'https://dvmn.org/api/long_polling/'
    while True:
        try:
            response = requests.get(
                url,
                headers=headers,
                params={'timestamp': 'timestamp'},
                timeout=90,
            )
            answer = response.json()
            if ('status',  'found') in answer.items():
                send_notifications(bot, answer, chat_id)
        except requests.exceptions.ReadTimeout:
            logger.error(f'ReadTimeout: Нет проверенных работ!')
        except requests.exceptions.ConnectionError:
            time.sleep(90)
            logger.error('ConnectionError: Нет подключения к интернету!')


def main():
    env = Env()
    env.read_env('.env')
    bot_api = env('TELEGRAM_TOKEN')
    dvm_api = env('DEVMAN_API')
    chat_id = env('TG_USER_CHAT_ID')
    bot = telegram.Bot(bot_api)
    headers = {
        'Authorization': dvm_api,
    }
    make_requests(headers, bot, chat_id)


if __name__ == '__main__':
    main()
