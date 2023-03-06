# api_yamdb
api yamdb

Как запустить проект:

Клонировать репозиторий и перейти в него в командной строке:
git clone вставть ссылку из GitHub


Затем нужно выполнить команду 
```
cd api_yamdb
```

Cоздать и активировать виртуальное окружение:
```
python -m venv venv
source venv/Scripts/activate
```

Установить зависимости из файла requirements.txt:

```
python -m pip install --upgrade pip
pip install -r requirements.txt
```


Выполнить миграции:

```
python manage.py migrate
```


Запустить проект:

```
python manage.py runserver
```