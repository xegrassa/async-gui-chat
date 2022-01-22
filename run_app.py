import asyncio
import logging
from tkinter import messagebox

from anyio import create_task_group
from dotenv import load_dotenv

from core import gui
from core.cli import parse_args
from core.const import Queue
from core.coroutines.connect import handle_connection
from core.coroutines.files import restore_history_from, save_messages
from core.exceptions import InvalidTokenError

logger = logging.getLogger(__name__)


async def main(host, listen_port, write_port, history_path, token):
    queues = Queue(asyncio.Queue(), asyncio.Queue(), asyncio.Queue(), asyncio.Queue(), asyncio.Queue())

    await restore_history_from(history_path, queues.messages)

    async with create_task_group() as tg:
        tg.start_soon(gui.draw, queues.messages, queues.sending, queues.status_updates)
        tg.start_soon(save_messages, history_path, queues.history)
        tg.start_soon(handle_connection, host, listen_port, write_port, queues, token)


def _configure_loggers():
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    formatter = logging.Formatter(f'%(levelname)s:%(module)s:%(message)s')
    ch.setFormatter(formatter)

    logging.getLogger('core.coroutines.chatter').setLevel(logging.DEBUG)
    logging.getLogger('core.coroutines.chatter').addHandler(ch)
    logging.getLogger('core.coroutines.access').setLevel(logging.DEBUG)
    logging.getLogger('core.coroutines.access').addHandler(ch)
    logging.getLogger('watchdog').setLevel(logging.DEBUG)
    logging.getLogger('watchdog').addHandler(ch)

    logger.setLevel(logging.DEBUG)
    logger.addHandler(ch)


if __name__ == '__main__':
    load_dotenv()
    _configure_loggers()
    args = parse_args()
    try:
        asyncio.run(main(args.host, args.listen_port, args.write_port, args.history, args.token))
    except InvalidTokenError:
        messagebox.showinfo("Неверный токен", "Проверьте токен, сервер его не узнал")
    except (gui.TkAppClosed, KeyboardInterrupt):
        print('Приложение закрыто')
