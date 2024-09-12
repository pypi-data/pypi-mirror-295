from __future__ import annotations

import aiormq

from krri_common.adapters.message_channel import MessageChannel


class MessageReceiver:
    def __init__(self, channel: MessageChannel, callback, host='localhost'):
        self._channel_name = str(channel)
        self._host = host
        self._callback = callback

    async def start(self):
        self.connection = await aiormq.connect(f"amqp://guest:guest@{self._host}/")
        self.channel = await self.connection.channel()
        declare_ok = await self.channel.queue_declare(queue=str(self._channel_name))

        async def wrapped_callback(message):
            await self._callback(message.body)

        consume_ok = await self.channel.basic_consume(declare_ok.queue, wrapped_callback, no_ack=True)
