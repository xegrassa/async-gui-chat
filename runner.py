import asyncio
import json
import logging
import time
from asyncio import StreamWriter, StreamReader
from pathlib import Path

import aiofiles
from dotenv import load_dotenv

from core.cli import parse_args
from core.coroutines.chatter import read_message, submit_message
from core.coroutines.connect import open_connection
from core.coroutines.files import add_msg_to_history
from core.exceptions import InvalidTokenError

logger = logging.getLogger(__name__)


async def main(host, listen_port,write_port, history_path, token):
    messages_queue = asyncio.Queue()
    sending_queue = asyncio.Queue()
    status_updates_queue = asyncio.Queue()
    history_queue = asyncio.Queue()

    await restore_history_from(history_path, messages_queue)

    async with open_connection(host, write_port) as conn:
        await sign_in(conn, token)
        # task_1 = gui.draw(messages_queue, sending_queue, status_updates_queue)
        # task_2 = read_msgs(conn, messages_queue, history_queue)
        # task_3 = save_messages(history_path, history_queue)
        # task_4 = send_msgs(conn, sending_queue)
        # await asyncio.gather(task_2, task_1, task_3, task_4)


async def restore_history_from(history_path: str, queue: asyncio.Queue):
    """Востанавливает историю в GUI из файла Логов истории"""
    if Path(history_path).exists():
        async with aiofiles.open(history_path, 'r', encoding='utf-8') as f:
            async for line in f:
                queue.put_nowait(line)


async def generate_msgs(queue: asyncio.Queue):
    """Отправка Ping в чат, скорее всего придется удалить."""
    while True:
        msg = f'Ping {int(time.time())}'
        queue.put_nowait(msg)
        await asyncio.sleep(1)


async def read_msgs(conn: tuple[StreamReader, StreamWriter], messages_queue: asyncio.Queue,
                    history_queue: asyncio.Queue):
    """
    Читает сообщения из чата Девман.

    Считанные сообщения отправляет в очередь на отображение GUI и очередь для записи в Лог переписки
    :param host: IP адресс - чата девман
    :param port: Порт - чата девман
    :param messages_queue: Очередь для отправки сообщений в GUI
    :param history_queue: Очередь для отправки сообщений в Логи
    """
    reader, _ = conn
    while True:
        msg = await read_message(reader)
        messages_queue.put_nowait(msg)
        history_queue.put_nowait(msg)


async def send_msgs(conn: tuple[StreamReader, StreamWriter], sending_queue: asyncio.Queue):
    _, writer = conn
    while True:
        msg = await sending_queue.get()
        print(msg)


async def save_messages(filepath, history_queue: asyncio.Queue):
    """
    Сохраняет сообщение в Лог.

    :param filepath: Путь до файла логов
    :param queue: Очередь для отправки сообщений в Логи
    """
    while True:
        msg = await history_queue.get()
        await add_msg_to_history(msg, filepath)


async def sign_in(conn: tuple[StreamReader, StreamWriter], token: str):
    """
    Авторизация в чате.

    :param conn: Кортеж из (StreamReader, StreamWriter) являющимися коннектом к чату девмана
    :param token: Токен для авторизации
    """
    reader, writer = conn
    await read_message(reader)
    await submit_message(writer, token)

    data = await read_message(reader)
    if json.loads(data) is None:
        raise InvalidTokenError

    logger.debug(data)
    await read_message(reader)


if __name__ == '__main__':
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

    load_dotenv()
    args = parse_args()
    print(args)
    asyncio.run(main(args.host, args.listen_port,args.write_port, args.history, args.token))
