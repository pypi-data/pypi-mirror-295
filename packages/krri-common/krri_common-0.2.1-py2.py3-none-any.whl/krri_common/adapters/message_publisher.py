from __future__ import annotations

import pika

from krri_common.adapters.message_channel import MessageChannel


class MessagePublisher:
    def __init__(self, channel: MessageChannel, host='localhost'):
        self._channel_name = str(channel)
        self._host = host
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host=self._host))
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue=str(channel))

    def publish(self, data: bytes | str):
        self.channel.basic_publish(exchange='', routing_key=self._channel_name, body=data)
