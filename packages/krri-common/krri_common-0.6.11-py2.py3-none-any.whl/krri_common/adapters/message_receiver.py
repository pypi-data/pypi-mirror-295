from __future__ import annotations

import logging

import aiormq

from krri_common.adapters.message_channel import MessageChannel


class MessageReceiver:
    def __init__(self, channel: MessageChannel, callback, host='localhost'):
        self._channel_name = str(channel)
        self._host = host
        self._callback = callback
        self.connection = None
        self.channel = None

    async def start(self):
        try:
            await self.create_connection()
        except aiormq.AMQPConnectionError as ac:
            logging.error(f"{ac!r}")
            await self.create_connection()

    async def create_connection(self):
        self.connection = await aiormq.connect(f"amqp://guest:guest@{self._host}/")
        self.channel = await self.connection.channel()
        await self.channel.basic_qos(prefetch_count=1)
        declare_ok = await self.channel.queue_declare(queue=str(self._channel_name))

        async def wrapped_callback(message: aiormq.abc.DeliveredMessage):
            await self._callback(message.body)
            await message.channel.basic_ack(
                message.delivery.delivery_tag
            )

        consume_ok = await self.channel.basic_consume(declare_ok.queue, wrapped_callback)
