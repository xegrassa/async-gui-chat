import asyncio
from pathlib import Path

import aiofiles


async def add_msg_to_history(message: str, path):
    """
    Запись сообщения в файл.
    :param message: Сообщение
    :param path: Путь до файла (Если файла нет то создастся)
    """
    async with aiofiles.open(path, mode='a', encoding='utf-8') as f:
        await f.write(message)


async def restore_history(history_path: str, queue: asyncio.Queue):
    """Востанавливает историю в GUI из файла Логов истории"""
    if Path(history_path).exists():
        async with aiofiles.open(history_path, 'r', encoding='utf-8') as f:
            async for line in f:
                queue.put_nowait(line)


async def save_messages(file_path, history_queue: asyncio.Queue):
    """
    Сохраняет сообщение в Лог.

    :param file_path: Путь до файла логов
    :param queue: Очередь для отправки сообщений в Логи
    """
    while True:
        msg = await history_queue.get()
        await add_msg_to_history(msg, file_path)


async def write_token(token: str, file_path: str):
    """
    Запись токена в файл.

    :param token: Токен
    :param file_path: Путь до файла (Если его нет то создастся)
    """
    async with aiofiles.open(file_path, 'w', encoding='utf-8') as f:
        await f.write(f'token = {token}')
