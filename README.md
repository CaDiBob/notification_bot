# Уведомления о проверке работ.

Телеграм бот шлет уведомления, если преподаватель проверил работу на курсе веб-разработки [DEVMAN](https://dvmn.org/)

### Как установить:

Python3 должен быть установлен, затем используйте `pip`

```bash
pip install -r requirements.txt
```

### Как запустить:

Для рассылки уведомлений использует telegram бота, [инструкция как создать бота](https://way23.ru/%D1%80%D0%B5%D0%B3%D0%B8%D1%81%D1%82%D1%80%D0%B0%D1%86%D0%B8%D1%8F-%D0%B1%D0%BE%D1%82%D0%B0-%D0%B2-telegram.html).

Для настройки используйте файл `.env`

Пример `.env`:
```
TELEGRAM_TOKEN='тг токен бота'
TG_USER_CHAT_ID='ваш чат id'
DEVMAN_API='токен к API devman'
```

Затем используйте:


```bash
python bot.py
```

### Сборка и запуск Docker контейнера:

Для запуска Docker контейнера на локальной машине [Docker должен быть установлен](https://docs.docker.com/get-docker/).

Клонировать репозиторий

```bash
git clone https://github.com/CaDiBob/notification_bot.git
cd notification_bot
```

Затем используйте следующие команды:

##### Собрать образ:

```bash
docker build /путь куда хотите собрать/ -t 'имя_контейнера:тэг'
```
##### Запуск образа:

```bash
docker run --env-file /путь до файла .env с переменными окружения/ 'имя_контейнера:тэг'
```
