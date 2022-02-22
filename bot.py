import logging
import requests
import telegram
import time

from environs import Env


logger = logging.getLogger('bot')


def send_notifications(bot, answer, chat_id):
    for attempt  in answer.get('new_attempts'):
        lesson_title = attempt.get('lesson_title')
        lesson_url = attempt.get('lesson_url')
        attempt = attempt.get('is_negative')
        if attempt:
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
    timestamp=time.time()
    while True:
        try:
            response = requests.get(
                url,
                headers=headers,
                params={'timestamp': timestamp},
                timeout=90,
            )
            answer = response.json()
            if ('status',  'found') in answer.items():
                timestamp = answer.get('last_attempt_timestamp')
                send_notifications(bot, answer, chat_id)
            else:
                timestamp = answer.get('timestamp_to_request')
        except requests.exceptions.ReadTimeout:
            pass
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
