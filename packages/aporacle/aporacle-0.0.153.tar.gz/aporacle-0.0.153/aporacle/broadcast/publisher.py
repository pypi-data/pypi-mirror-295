import asyncio
import json
import logging
from typing import Optional

import websockets
from komoutils.core import safe_ensure_future, KomoBase


class Publisher(KomoBase):
    def __init__(self, url: str, stream: str):
        self.stream = stream
        self.url: str = url
        self.send_data_stream: asyncio.Queue = asyncio.Queue()
        self.run_task: Optional[asyncio.Task] = None
        self.protocol = "ws://"

    @property
    def name(self):
        return f"publisher_{self.stream}".lower()

    def start(self):
        self.url = f"{self.protocol}{self.url}/ingest"
        self.run_task = safe_ensure_future(self.run())
        self.log_with_clock(log_level=logging.INFO, msg=f"Started {self.name}. ".upper())

    def stop(self):
        pass

    async def run(self):
        self.log_with_clock(log_level=logging.INFO, msg=f"Connecting to {self.url} for the {self.stream} data stream. ")
        try:
            async with websockets.connect(self.url) as ws:
                self.log_with_clock(log_level=logging.INFO,
                                    msg=f"Connection to {self.url} for {self.stream} data is now active. ")
                while True:
                    message: dict = await self.send_data_stream.get()
                    await ws.send(json.dumps(message.copy()))
                    self.send_data_stream.task_done()

        except Exception as e:
            self.log_with_clock(log_level=logging.ERROR, msg=f"Connection was closed. Will retry {e}")
            await asyncio.sleep(1)
            safe_ensure_future(self.run())
