import json
from asyncio import StreamReader, StreamWriter

from core.coroutines.chatter import read_message, submit_message
from core.exceptions import InvalidTokenError


async def sign_in(conn: tuple[StreamReader, StreamWriter], token: str) -> dict:
    """
    Авторизация в чате.

    :param conn: Кортеж из (StreamReader, StreamWriter) являющимися коннектом к чату девмана
    :param token: Токен для авторизации
    """
    reader, writer = conn
    await read_message(reader)
    await submit_message(writer, token)

    data = await read_message(reader)
    if json.loads(data) is None:
        raise InvalidTokenError

    await read_message(reader)
    await read_message(reader)
    return json.loads(data)


async def sign_up(conn: tuple[StreamReader, StreamWriter], name: str) -> str:
    """
    Регистрация нового пользователя в чате и получение токена.

    :param conn: Кортеж из (StreamReader, StreamWriter) являющимися коннектом к чату девмана
    :param name: Имя пользователя
    :return: Токен
    """
    reader, writer = conn
    await read_message(reader)
    await submit_message(writer)
    await read_message(reader)
    await submit_message(writer, name)
    message = await read_message(reader)

    _, token = json.loads(message).values()
    return token
