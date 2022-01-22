import asyncio
import socket
from asyncio import StreamReader, StreamWriter
from contextlib import asynccontextmanager
from typing import Tuple


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


def reconnect(coro):
    """Декоратор для реконекта."""

    async def wrapped(*args, **kwargs):
        while True:
            try:
                await coro(*args, **kwargs)
            except (ConnectionError, socket.gaierror):
                await asyncio.sleep(2)
            print('Попытка Реконекта')

    return wrapped