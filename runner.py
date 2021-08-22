import asyncio
import time
from pathlib import Path

from dotenv import load_dotenv

import gui
from core.cli import parse_args
from core.coroutines.chatter import read_message
from core.coroutines.connect import open_connection
from core.coroutines.files import add_msg_to_history


def restore_history_from(history_path: str, queue: asyncio.Queue):
    if Path(history_path).exists():
        with open(history_path, 'r', encoding='utf-8') as f:
            for line in f:
                queue.put_nowait(line)


async def main(host, port, history_path):
    messages_queue = asyncio.Queue()
    sending_queue = asyncio.Queue()
    status_updates_queue = asyncio.Queue()
    history_queue = asyncio.Queue()

    restore_history_from(history_path, messages_queue)

    task_1 = gui.draw(messages_queue, sending_queue, status_updates_queue)
    task_2 = read_msgs(host, port, messages_queue, history_queue)
    task_3 = save_messages(history_path, history_queue)
    await asyncio.gather(task_2, task_1, task_3)


async def generate_msgs(queue: asyncio.Queue):
    """Отправка Ping в чат, скорее всего придется удалить."""
    while True:
        msg = f'Ping {int(time.time())}'
        queue.put_nowait(msg)
        await asyncio.sleep(1)


async def read_msgs(host, port, messages_queue: asyncio.Queue, history_queue: asyncio.Queue):
    async with open_connection(host, port) as (reader, _):
        while True:
            msg = await read_message(reader)
            messages_queue.put_nowait(msg)
            history_queue.put_nowait(msg)


async def save_messages(filepath, queue: asyncio.Queue):
    while True:
        msg = await queue.get()
        await add_msg_to_history(msg, filepath)


if __name__ == '__main__':
    load_dotenv()
    args = parse_args()
    asyncio.run(main(args.host, args.port, args.history))
