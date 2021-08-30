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
