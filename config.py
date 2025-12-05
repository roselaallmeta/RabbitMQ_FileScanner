"""
Configuration settings for RabbitMQ connection.
"""

RABBITMQ_HOST = 'localhost'
RABBITMQ_PORT = 5672
RABBITMQ_USERNAME = 'guest'
RABBITMQ_PASSWORD = 'guest'
RABBITMQ_VIRTUAL_HOST = '/'


DEFAULT_QUEUE = 'norcom_queue'
DEFAULT_EXCHANGE = 'norcom_exchange'
DEFAULT_ROUTING_KEY = 'norcom.routing.key'

