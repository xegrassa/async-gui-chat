import asyncio
from tkinter import *
from tkinter import messagebox

from dotenv import load_dotenv

from core import gui
from core.cli import parse_args
from core.coroutines.autorisation import sign_up
from core.coroutines.decorators_and_managers import open_connection
from core.coroutines.files import write_token


async def user_registration(host, port, user_name):
    """Регистрация нового пользователя и запись его токена в файл."""
    async with open_connection(host, port) as conn:
        token = await sign_up(conn, user_name)
    await write_token(token, 'token.txt')
    messagebox.showinfo("Токен сохранен", token)


def registration_event(entry, host, port):
    """Обработчик события нажатие на кнопку 'Зарегистрироваться'."""
    name = entry.get()
    asyncio.run(user_registration(host, port, name))


def main(args):
    root = Tk()
    root.title('Регистрация нового пользователя')
    root.geometry("370x150")

    label = Label(text="Введите имя для регистрации")
    entry = Entry(width=50, bd=2)

    button = Button(width=30, height=3, bd=4)
    button["text"] = "Зарегистрироваться"
    button["command"] = lambda: registration_event(entry, args.host, args.write_port)

    label.pack()
    entry.pack()
    button.pack()
    root.mainloop()


if __name__ == '__main__':
    load_dotenv()
    args = parse_args()
    try:
        main(args)
    except (gui.TkAppClosed, KeyboardInterrupt):
        print('Приложение закрыто')
