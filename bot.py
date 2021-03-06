import logging
import requests
import telegram
import time

from environs import Env


logger = logging.getLogger('bot')


class TelegramLogsHandler(logging.Handler):

    def __init__(self, chat_id, bot):
        super().__init__()
        self.chat_id = chat_id
        self.tg_bot = bot

    def emit(self, record):
        log_entry = self.format(record)
        self.tg_bot.send_message(chat_id=self.chat_id, text=log_entry)



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
            response.raise_for_status()
            answer = response.json()
            if answer.get('status')=='found':
                timestamp = answer.get('last_attempt_timestamp')
                send_notifications(bot, answer, chat_id)
            else:
                timestamp = answer.get('timestamp_to_request')
        except requests.exceptions.ReadTimeout:
            pass
        except requests.exceptions.ConnectionError:
            logger.exception('Нет подключения к интернету!')
            time.sleep(90)


def main():
    env = Env()
    env.read_env('.env')
    bot_api = env('TELEGRAM_TOKEN')
    dvm_api = env('DEVMAN_API')
    chat_id = env('TG_USER_CHAT_ID')
    bot = telegram.Bot(bot_api)
    logger.setLevel(logging.INFO)
    headers = {
        'Authorization': dvm_api,
    }
    logger.addHandler(TelegramLogsHandler(chat_id, bot))
    logger.info('Бот запущен!')
    make_requests(headers, bot, chat_id)

if __name__ == '__main__':
    main()
