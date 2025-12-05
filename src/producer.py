"""
RabbitMQ Producer module for sending messages to RabbitMQ queues.
"""
import json
import pika
from typing import Dict, Any

from config import (
    RABBITMQ_HOST,
    RABBITMQ_PORT,
    RABBITMQ_USERNAME,
    RABBITMQ_PASSWORD,
    RABBITMQ_VIRTUAL_HOST,
    DEFAULT_QUEUE,
    DEFAULT_EXCHANGE,
    DEFAULT_ROUTING_KEY
)


class RabbitMQProducer:
    """RabbitMQ producer for publishing messages to queues."""
    
    def __init__(self, queue: str = None):
        """Initialize RabbitMQ producer."""
        self.queue = queue or DEFAULT_QUEUE
        self.connection = None
        self.channel = None
    
    def connect(self):
        """Establish connection to RabbitMQ."""
        credentials = pika.PlainCredentials(RABBITMQ_USERNAME, RABBITMQ_PASSWORD)
        parameters = pika.ConnectionParameters(
            host=RABBITMQ_HOST,
            port=RABBITMQ_PORT,
            virtual_host=RABBITMQ_VIRTUAL_HOST,
            credentials=credentials
        )
        
        self.connection = pika.BlockingConnection(parameters)
        self.channel = self.connection.channel()
        
        # Declare exchange and queue
        self.channel.exchange_declare(exchange=DEFAULT_EXCHANGE, exchange_type='direct', durable=True)
        self.channel.queue_declare(queue=self.queue, durable=True)
        self.channel.queue_bind(
            exchange=DEFAULT_EXCHANGE,
            queue=self.queue,
            routing_key=DEFAULT_ROUTING_KEY
        )
    
    def publish_message(self, message: Dict[str, Any]) -> bool:
        """Publish a message to RabbitMQ queue as JSON."""
        try:
            message_body = json.dumps(message)
            
            self.channel.basic_publish(
                exchange=DEFAULT_EXCHANGE,
                routing_key=DEFAULT_ROUTING_KEY,
                body=message_body,
                properties=pika.BasicProperties(
                    delivery_mode=2,  # Make message persistent
                    content_type='application/json'
                )
            )
            return True
        except Exception as e:
            print(f"Error publishing message: {e}")
            return False
    
    def close(self):
        """Close RabbitMQ connection."""
        if self.channel:
            self.channel.close()
        if self.connection:
            self.connection.close()

