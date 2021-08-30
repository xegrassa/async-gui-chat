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


async def restore_history_from(history_path: str, queue: asyncio.Queue):
    """Востанавливает историю в GUI из файла Логов истории"""
    if Path(history_path).exists():
        async with aiofiles.open(history_path, 'r', encoding='utf-8') as f:
            async for line in f:
                queue.put_nowait(line)


async def save_messages(filepath, history_queue: asyncio.Queue):
    """
    Сохраняет сообщение в Лог.

    :param filepath: Путь до файла логов
    :param queue: Очередь для отправки сообщений в Логи
    """
    while True:
        msg = await history_queue.get()
        await add_msg_to_history(msg, filepath)