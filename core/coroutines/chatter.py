import asyncio
import logging
from asyncio import StreamWriter, StreamReader

from core import Notification
from core.const import Queue

logger = logging.getLogger(__name__)


async def submit_message(writer: StreamWriter, message: str = ''):
    """
    Отправляет сообщение в чат Девман.
    :param writer: Экземпляр  asyncio.StreamWriter
    :param message: Текст сообщения
    """
    send_message = message.replace('\n', '')
    logger.debug(f'SEND: {send_message}')
    writer.write((send_message + '\n\n').encode())
    await writer.drain()


async def read_message(reader: StreamReader) -> str:
    """
    Читает сообщение из чата Девман.
    :param reader: Экземпляр  asyncio.StreamReader
    :return: Полученное Сообщение
    """
    response = await reader.readline()
    logger.debug(f'READ: {response.decode()}')
    return response.decode()


async def read_msgs(conn: tuple[StreamReader, StreamWriter], queues: Queue):
    """
    Читает сообщения из чата Девман.

    Считанные сообщения отправляет в очередь на отображение GUI и очередь для записи в Лог переписки
    """
    reader, _ = conn
    while True:
        msg = await read_message(reader)
        await asyncio.sleep(0.1)
        queues.messages.put_nowait(msg)
        queues.history.put_nowait(msg)
        queues.watchdog.put_nowait(Notification.NEW_MESSAGE_IN_CHAT)


async def send_msgs(conn: tuple[StreamReader, StreamWriter], queues: Queue):
    """Посылает сообщение в чат Девмана."""
    _, writer = conn
    while True:
        msg = await queues.sending.get()
        await submit_message(writer=writer, message=msg)
        queues.watchdog.put_nowait(Notification.MESSAGE_SENT)
