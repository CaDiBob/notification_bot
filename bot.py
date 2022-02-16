import logging
import requests
import telegram
import time

from environs import Env


logger = logging.getLogger('bot')


def send_message(bot, answer, chat_id):
    for elem in answer.get('new_attempts'):
        lesson_title = elem.get('lesson_title')
        lesson_url = elem.get('lesson_url')
        result = elem.get('is_negative')
        if result:
            bot.send_message(
                text=f'''Преподаватель проверил работу "{lesson_title}"
                \nссылка: {lesson_url}
                \nЕсть ошибки, работа не принята.''',
                chat_id=chat_id,
            )
        else:
            bot.send_message(
                text=f'''Преподаватель проверил работу "{lesson_title}"
                \nссылка {lesson_url}
                \nОшибок нет, работа принята''',
                chat_id=chat_id,
            )


def polls(url, headers, bot, chat_id):
    while True:
        timestamp = int(time.time())
        try:
            response = requests.get(
                url,
                headers=headers,
                params={'timestamp': timestamp}
            )
            answer = response.json()
            if answer.get('new_attempts'):
                send_message(bot, answer, chat_id)
        except requests.exceptions.ReadTimeout:
            logger.error(f'ReadTimeout: Нет проверенных работ!')
        except requests.exceptions.ConnectionError:
            logger.error('ConnectionError: Нет подключения к интернету!')


def main():
    env = Env()
    env.read_env('.env')
    bot_api = env('TELEGRAM_TOKEN')
    devm_api = env('DEVMAN_API')
    chat_id = env('TG_USER_CHAT_ID')
    bot = telegram.Bot(bot_api)
    url = 'https://dvmn.org/api/long_polling/'
    headers = {
        'Authorization': devm_api,
    }
    polls(url, headers, bot, chat_id)


if __name__ == '__main__':
    main()
