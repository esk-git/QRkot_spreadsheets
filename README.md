# QRkot_spreadseets
Приложение для Благотворительного фонда поддержки котиков
Может быть открыто несколько целевых проектов. У каждого проекта есть название, описание и сумма, которую планируется собрать. После того, как нужная сумма собрана — проект закрывается.
Пожертвования в проекты поступают по принципу First In, First Out: все пожертвования идут в проект, открытый раньше других; когда этот проект набирает необходимую сумму и закрывается — пожертвования начинают поступать в следующий проект.
Реализована возможность формирования отчёта в гугл-таблице. В таблицу попадают закрытые проекты, отсортированные по скорости сбора средств: от тех, что закрылись быстрее всего, до тех, что долго собирали нужную сумму.
## Используемые технологии
В данном проекте были применены следующие технологии:

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54) ![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)
## Как запустить проект
- Клонировать репозиторий
```
git clone https://github.com/esk-git/QRkot_spreadsheets.git
```
```
cd QRkot_spreadsheets
```

- Cоздать и активировать виртуальное окружение:

```
python3 -m venv venv
```
![Windows](https://img.shields.io/badge/Windows-0078D6?style=for-the-badge&logo=windows&logoColor=white)
```
source venv/scripts/activate
```
![macOS](https://img.shields.io/badge/mac%20os-000000?style=for-the-badge&logo=macos&logoColor=F0F0F0) ![Linux](https://img.shields.io/badge/Linux-FCC624?style=for-the-badge&logo=linux&logoColor=black)
```
source venv/bin/activate
```

- Установить зависимости из файла requirements.txt:

```
python3 -m pip install --upgrade pip
```

```
pip install -r requirements.txt
```
- Создать в корневой директории файл .env
```
nano .env
```
- Заполнить его
```
APP_TITLE=Благотворительный фонд поддержки котиков QRKot
APP_DESCRIPTION=Больше котиков богу **котиков**
DATABASE_URL=sqlite+aiosqlite:///./fastapi.db
SECRET=SECRET_WORD
```
- Выполнить миграции:
```
alembic upgrade head
```
- Запустить проект:
```
uvicorn app.main:app
```
Открыть [страницу](http://127.0.0.1:8000/docs)
```
http://127.0.0.1:8000/docs
```
### Работа с Google таблицами
Сформировать таблицу можно отправив GET запрос на эндпоинт
```
/google
```
Для работы эндпоинта необходимо создать .env файл со следующими данными:
```
EMAIL=
TYPE=service_account
PROJECT_ID=
PRIVATE_KEY_ID=
PRIVATE_KEY=
CLIENT_EMAIL=
CLIENT_ID=
AUTH_URI=
TOKEN_URI=
AUTH_PROVIDER_X509_CERT_URL=
CLIENT_X509_CERT_URL=
UNIVERSE_DOMAIN=
```
Все константы можно перенести в .env файл из json файла, который вы скачиваете при создании сервисного аккаунта в Google API. 

#### Автор
Каликов Евгений

![Jokes Card](https://readme-jokes.vercel.app/api)
