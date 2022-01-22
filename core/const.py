import asyncio
from dataclasses import dataclass


@dataclass
class Queue:
    messages: asyncio.Queue
    sending: asyncio.Queue
    status_updates: asyncio.Queue
    history: asyncio.Queue
    watchdog: asyncio.Queue
