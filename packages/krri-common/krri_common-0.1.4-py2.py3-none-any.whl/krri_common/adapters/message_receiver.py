from __future__ import annotations

from typing import Callable

import pika

from krri_common.adapters.message_channel import MessageChannel


class MessageReceiver:
    def __init__(self, channel: MessageChannel, callback: Callable[[bytes], None], host='localhost'):
        self._channel_name = str(channel)
        self._host = host
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host=self._host))
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue=str(channel))

        def wrapped_callback(ch, method, properties, body):
            callback(body)

        self.channel.basic_consume(queue=str(channel), on_message_callback=wrapped_callback, auto_ack=True)
