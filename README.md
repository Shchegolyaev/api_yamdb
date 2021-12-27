# API_YAMDB
## Описание
Сервис REST API проекта Yatube
## Установка

Создать и активировать виртуальное окружение:

```sh
python3 -m venv venv
source venv/bin/activate
```
Установить зависимости из файла requirements.txt:
```sh
python3 -m pip install --upgrade pip
pip install -r requirements.txt
```
Выполнить миграции:
```sh
python3 manage.py migrate
```

Запуск:
```sh
python3 manage.py runserver
```

## Документация
```sh
http://127.0.0.1:8000/redoc/
```

## Требования
* Python 3.7
* Django 2.2
* PyJWT 2.1.0
