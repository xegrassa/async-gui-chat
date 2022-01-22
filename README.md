# Графический клиент для чата Девман

### Установка
Клонируйте проект и установите зависимости командами ниже. Для работы требуется версия Python 3.9 +
```
git clone https://github.com/xegrassa/async-gui-chat.git
cd async-gui-chat
pip install -r requirements.txt
```

После установки доступно 2 скрипта: 
- [run_registration](#регистрация-нового-пользователя)
- [run_app](#запуск-GUI-клиента-чата)


***

### Регистрация нового пользователя
Для регистрации нового пользователя запустите скрипт: 

`python run_registration.py`

![img](https://user-images.githubusercontent.com/52129535/150636950-95d81e4e-0396-4d06-a9e4-7249fda838a8.png)

После ввода имени и нажатия на кнопку. Полученный Токен сохраниться в файл **token.txt** в корне проекта
![token](https://user-images.githubusercontent.com/52129535/150636955-d4e3e039-0e97-457b-80f0-b81820989826.png)

***
### Запуск GUI клиента чата
Для запуска GUI клиента чата Девман запустите скрипт: 

`python run_app.py`

![img_1](https://user-images.githubusercontent.com/52129535/150636954-44518679-117f-4b34-a6f8-48ef5465a6ea.png)

Чат логируется в файл **minechat.log** в корне проекта

***
### .env
Параметры подключения можно изменить добавив в окружение переменные или передать через *.env* файл созданный в корне приложения
```
HOST = 192.168.0.1
LISTEN_PORT = 1234
WRITE_PORT = 1234
HISTORY = ./minechat.log
TOKEN = abc123qwe456
```
***
### Requirements
- [Python 3.9+](https://www.python.org/)
- [aiofiles](https://github.com/Tinche/aiofiles)
- [anyio](https://github.com/agronholm/anyio)
- [async-timeout](https://github.com/aio-libs/async-timeout)
- [ConfigArgParse](https://github.com/bw2/ConfigArgParse)
- [python-dotenv](https://github.com/theskumar/python-dotenv)
