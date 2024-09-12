from __future__ import annotations

import logging

import pika
from krri_common.adapters.message_channel import MessageChannel


class MessagePublisher:
    def __init__(self, channel: MessageChannel, host='localhost'):
        self._channel_name = str(channel)
        self._host = host
        self.connection = None
        self.channel = None
        self._connect()

    def _connect(self):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host=self._host))
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue=self._channel_name)

    def publish(self, data: bytes | str):
        try:
            self.channel.basic_publish(exchange='', routing_key=self._channel_name, body=data)
        except Exception as e:
            logging.error(f'{e!r}')
            self._connect()

    def delete_all_message(self):
        try:
            while True:
                method_frame, header_frame, body = self.channel.basic_get(queue=self._channel_name)
                if method_frame:
                    self.channel.basic_ack(delivery_tag=method_frame.delivery_tag)
                    logging.debug(f"[+] Message deleted on channel {self._channel_name}")
                else:
                    break
        except Exception as e:
            logging.error(f"{e!r}")
