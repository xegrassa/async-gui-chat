import asyncio
import logging
from asyncio import StreamWriter, StreamReader
from core import Notification
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


async def read_msgs(conn: tuple[StreamReader, StreamWriter], messages_queue: asyncio.Queue,
                    history_queue: asyncio.Queue, watchdog_queue: asyncio.Queue):
    """
    Читает сообщения из чата Девман.

    Считанные сообщения отправляет в очередь на отображение GUI и очередь для записи в Лог переписки
    :param conn
    : IP адресс - чата девман
    :param port: Порт - чата девман
    :param messages_queue: Очередь для отправки сообщений в GUI
    :param history_queue: Очередь для отправки сообщений в Логи
    """
    reader, _ = conn
    while True:
        msg = await read_message(reader)
        await asyncio.sleep(0.1)
        messages_queue.put_nowait(msg)
        history_queue.put_nowait(msg)
        watchdog_queue.put_nowait(Notification.NEW_MESSAGE_IN_CHAT)


async def send_msgs(conn: tuple[StreamReader, StreamWriter], sending_queue: asyncio.Queue, watchdog_queue):
    """
    Посылает сообщение в чат Девмана.

    :param conn:
    :param sending_queue:
    :return:
    """
    _, writer = conn
    while True:
        msg = await sending_queue.get()
        await submit_message(writer=writer, message=msg)
        watchdog_queue.put_nowait(Notification.MESSAGE_SENT)
