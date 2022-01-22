import asyncio
import logging
import socket
import time
from asyncio import StreamReader, StreamWriter

from anyio import create_task_group
from async_timeout import timeout

from core import Notification, gui
from core.const import Queue
from core.coroutines.autorisation import sign_in
from core.coroutines.chatter import read_msgs, send_msgs
from core.coroutines.decorators_and_managers import open_connection, reconnect

watchdog_logger = logging.getLogger('watchdog')


async def watch_for_connection(queues: Queue):
    """Следит за состоянием соединений с помощью сообщений в очередях."""
    while True:

        try:
            async with timeout(5) as cm:
                notification = await queues.watchdog.get()
        except asyncio.TimeoutError:
            watchdog_logger.debug('5s timeout is elapsed')
            raise ConnectionError
        timestamp = int(time.time())
        if notification is Notification.NEW_MESSAGE_IN_CHAT:
            watchdog_logger.debug(f'watchdog_logger| [{timestamp}] Connection is alive. New message in chat')
        if notification is Notification.MESSAGE_SENT:
            watchdog_logger.debug(f'watchdog_logger| [{timestamp}] Connection is alive. Message sent')
        if notification is Notification.AUTHORIZATION_DONE:
            watchdog_logger.debug(f'watchdog_logger| [{timestamp}] Connection is alive. Authorization done')
        if notification is Notification.PROMPT_BEFORE_AUTH:
            watchdog_logger.debug(f'watchdog_logger| [{timestamp}] Connection is alive. Prompt before auth')


async def ping_pong(conn: tuple[StreamReader, StreamWriter], queues: Queue):
    """
    Посылает запрос каждые 2 секунды.

    При получении ответа отправляет уведомление в wathdog
    """
    reader, writer = conn
    while True:
        try:
            writer.write(b'\n')
            await writer.drain()
            await reader.readline()
            queues.watchdog.put_nowait(Notification.NEW_MESSAGE_IN_CHAT)
        except socket.gaierror:
            pass
        await asyncio.sleep(2)


@reconnect
async def handle_connection(host, listen_port, write_port, queues: Queue, token=''):
    """
    Собирает в себе всю логику взаимодействия с сервером.

    Управления сетевым соединением
    """
    queues.status_updates.put_nowait(gui.SendingConnectionStateChanged.INITIATED)
    queues.status_updates.put_nowait(gui.ReadConnectionStateChanged.INITIATED)
    async with open_connection(host, write_port) as conn:
        async with open_connection(host, listen_port) as conn_2:
            queues.status_updates.put_nowait(gui.SendingConnectionStateChanged.ESTABLISHED)
            queues.status_updates.put_nowait(gui.ReadConnectionStateChanged.ESTABLISHED)

            queues.watchdog.put_nowait(Notification.PROMPT_BEFORE_AUTH)
            response = await sign_in(conn, token)
            queues.watchdog.put_nowait(Notification.AUTHORIZATION_DONE)

            queues.status_updates.put_nowait(gui.NicknameReceived(response['nickname']))
            ok_msg = f"Выполнена авторизация. Пользователь {response['nickname']}."
            queues.messages.put_nowait(ok_msg)

            try:
                async with create_task_group() as tg:
                    tg.start_soon(read_msgs, conn_2, queues)
                    tg.start_soon(send_msgs, conn, queues)
                    tg.start_soon(watch_for_connection, queues)
                    tg.start_soon(ping_pong, conn, queues)
            except ConnectionError:
                queues.status_updates.put_nowait(gui.ReadConnectionStateChanged.CLOSED)
                queues.status_updates.put_nowait(gui.SendingConnectionStateChanged.CLOSED)
                raise
