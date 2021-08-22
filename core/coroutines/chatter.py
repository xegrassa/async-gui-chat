import logging
from asyncio import StreamWriter, StreamReader

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