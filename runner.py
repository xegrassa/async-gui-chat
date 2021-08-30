import asyncio
import logging
from tkinter import messagebox

from dotenv import load_dotenv

from core import gui, Notification
from core.cli import parse_args
from core.coroutines.autorisation import sign_in
from core.coroutines.chatter import read_msgs, send_msgs
from core.coroutines.connect import open_connection, watch_for_connection
from core.coroutines.files import restore_history_from, save_messages
from core.exceptions import InvalidTokenError

logger = logging.getLogger(__name__)


async def main(host, listen_port, write_port, history_path, token):
    messages_queue = asyncio.Queue()
    sending_queue = asyncio.Queue()
    status_updates_queue = asyncio.Queue()
    history_queue = asyncio.Queue()
    watchdog_queue = asyncio.Queue()

    await restore_history_from(history_path, messages_queue)

    async with open_connection(host, write_port) as conn:
        status_updates_queue.put_nowait(gui.SendingConnectionStateChanged.ESTABLISHED)
        watchdog_queue.put_nowait(Notification.PROMPT_BEFORE_AUTH)
        response = await sign_in(conn, token)
        watchdog_queue.put_nowait(Notification.AUTHORIZATION_DONE)

        status_updates_queue.put_nowait(gui.NicknameReceived(response['nickname']))
        ok_msg = f"Выполнена авторизация. Пользователь {response['nickname']}."
        messages_queue.put_nowait(ok_msg)

        async with open_connection(host, listen_port) as conn_2:
            status_updates_queue.put_nowait(gui.ReadConnectionStateChanged.ESTABLISHED)
            task_1 = gui.draw(messages_queue, sending_queue, status_updates_queue)
            task_2 = read_msgs(conn_2, messages_queue, history_queue, watchdog_queue)
            task_3 = save_messages(history_path, history_queue)
            task_4 = send_msgs(conn, sending_queue, watchdog_queue)
            task_5 = watch_for_connection(watchdog_queue)
            await asyncio.gather(task_1, task_2, task_3, task_4, task_5)


def _configure_loggers():
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(levelname)s:%(module)s:%(message)s')
    ch.setFormatter(formatter)

    logging.getLogger('core.coroutines.chatter').setLevel(logging.DEBUG)
    logging.getLogger('core.coroutines.chatter').addHandler(ch)
    logging.getLogger('core.coroutines.access').setLevel(logging.DEBUG)
    logging.getLogger('core.coroutines.access').addHandler(ch)

    logger.setLevel(logging.DEBUG)
    logger.addHandler(ch)


if __name__ == '__main__':
    _configure_loggers()
    load_dotenv()
    args = parse_args()
    print(args)
    try:
        asyncio.run(main(args.host, args.listen_port, args.write_port, args.history, args.token))
    except InvalidTokenError:
        messagebox.showinfo("Неверный токен", "Проверьте токен, сервер его не узнал")
    except gui.TkAppClosed:
        print('Приложение закрыто')
