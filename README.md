# API_YAMDB
## Описание
Это упрощенный проект Yatube в который добавлена работа API
## Установка

Создать и активировать виртуальное окружение:

```sh
python3 -m venv env
source env/bin/activate
```
Установить зависимости из файла requirements.txt:
```sh
python3 -m pip install --upgrade pip
pip install -r requirements.txt
```
Выполнить миграции:


```sh
python3 manage.py migrate
python3 manage.py runserver
```

## Примеры
При запуске проекта примеры запросов будут доступны по адресу:
```sh
http://127.0.0.1:8000/redoc/
```