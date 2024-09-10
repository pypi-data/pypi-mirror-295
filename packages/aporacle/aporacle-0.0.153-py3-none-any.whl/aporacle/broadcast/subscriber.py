import asyncio
import json
import logging
from typing import Optional

import websockets
from komoutils.core import KomoBase, safe_ensure_future
from pydantic import BaseModel


class SubscribeRequest(BaseModel):
    type: str = ""
    topics: list = []
    heartbeat: bool = True


class Subscriber(KomoBase):
    def __init__(self, url: str, stream: str, topics: list):
        self.stream = stream
        self.topics = topics
        self.url: str = url
        self.output: asyncio.Queue = asyncio.Queue()
        self.run_task: Optional[asyncio.Task] = None
        self.protocol = "ws://"

    @property
    def name(self):
        return f"subscriber_{self.output}".lower()

    def start(self):
        self.url = f"{self.protocol}{self.url}/subscribe"
        self.run_task = safe_ensure_future(self.run())
        self.log_with_clock(log_level=logging.INFO, msg=f"Started {self.name}. ".upper())

    def stop(self):
        pass

    async def run(self):
        self.log_with_clock(log_level=logging.INFO, msg=f"Connecting to {self.url} for the {self.stream} data stream. ")

        try:
            async with websockets.connect(self.url) as websocket:
                self.log_with_clock(log_level=logging.INFO,
                                    msg=f"Connection to {self.url} for {self.stream} data is now active. ")

                await websocket.send(json.dumps(SubscribeRequest(type='subscribe', topics=self.topics).dict()))

                while True:
                    try:
                        data = await websocket.recv()
                        message = json.loads(data)
                        if 'warning' in message:
                            self.log_with_clock(log_level=logging.WARNING, msg=f"{message['warning']}. ")
                            continue

                        if 'success' in message:
                            self.log_with_clock(log_level=logging.INFO, msg=f"{message['success']}. ")
                            continue

                        # self.log_with_clock(log_level=logging.INFO, msg=f"Received message topic {message['topic']} from {self.url}. ")
                        self.output.put_nowait(message)

                    except Exception as e:
                        self.log_with_clock(log_level=logging.ERROR,
                                            msg=f"Connection to {self.url} has failed. On message - {e}. ")
                        await asyncio.sleep(1)
                        safe_ensure_future(self.run())
        except Exception as e:
            self.log_with_clock(log_level=logging.ERROR, msg=f"Connection was closed. Will retry {e}")
            await asyncio.sleep(1)
            safe_ensure_future(self.run())
