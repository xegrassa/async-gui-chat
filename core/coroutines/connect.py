import asyncio
import time
from asyncio import StreamReader, StreamWriter
from contextlib import asynccontextmanager
from typing import Tuple

from core import Notification


@asynccontextmanager
async def open_connection(host, port) -> Tuple[StreamReader, StreamWriter]:
    """
    Контекст для открытия Асинхронного соединения и последующее его закрытие.
    :param host: IP
    :param port: Port
    :return: Reader, Writer
    """
    reader, writer = await asyncio.open_connection(host, port)
    try:
        yield reader, writer
    finally:
        writer.close()
        await writer.wait_closed()


async def watch_for_connection(watchdog_queue: asyncio.Queue):
    while True:
        notification = await watchdog_queue.get()

        timestamp = int(time.time())
        if notification is Notification.NEW_MESSAGE_IN_CHAT:
            print(f'[{timestamp}] Connection is alive. New message in chat')
        if notification is Notification.MESSAGE_SENT:
            print(f'[{timestamp}] Connection is alive. Message sent')
        if notification is Notification.AUTHORIZATION_DONE:
            print(f'[{timestamp}] Connection is alive. Authorization done')
        if notification is Notification.PROMPT_BEFORE_AUTH:
            print(f'[{timestamp}] Connection is alive. Prompt before auth')
