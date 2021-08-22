import asyncio
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