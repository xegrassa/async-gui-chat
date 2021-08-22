import asyncio
import gui
import time


async def main():
    messages_queue = asyncio.Queue()
    sending_queue = asyncio.Queue()
    status_updates_queue = asyncio.Queue()
    task_1 = gui.draw(messages_queue, sending_queue, status_updates_queue)
    task_2 = generate_msgs(messages_queue)
    # task_3 = read_msgs(messages_queue)
    await asyncio.gather(task_2, task_1)

    # loop = asyncio.get_event_loop()
    # loop.run_until_complete(gui.draw(messages_queue, sending_queue, status_updates_queue))


async def generate_msgs(queue: asyncio.Queue):
    while True:
        msg = f'Ping {int(time.time())}'
        queue.put_nowait(msg)
        await asyncio.sleep(1)


async def read_msgs(queue: asyncio.Queue):
    """
    Тестовая, удалить
    """
    while True:
        msg = queue.get_nowait()
        print(queue.qsize())
        print(msg)
        await asyncio.sleep(2)


if __name__ == '__main__':
    asyncio.run(main())
