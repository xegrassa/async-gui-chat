import aiofiles


async def add_msg_to_history(message: str, path):
    """
    Запись сообщения в файл.
    :param message: Сообщение
    :param path: Путь до файла (Если файла нет то создастся)
    """
    async with aiofiles.open(path, mode='a', encoding='utf-8') as f:
        await f.write(message)
