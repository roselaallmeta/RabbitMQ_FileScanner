"""
Tests for producer module.
"""
from src.producer import RabbitMQProducer
import pytest
from unittest.mock import Mock, patch, MagicMock



@patch('src.producer.pika.BlockingConnection')
def test_producer_initialization(mock_connection):
    """Test RabbitMQProducer initialization."""
    producer = RabbitMQProducer()
    assert producer.queue is not None
    assert producer.connection is None
    assert producer.channel is None


@patch('src.producer.pika.BlockingConnection')
def test_producer_custom_params(mock_connection_class):
    """Test producer with custom parameters."""
    mock_connection = MagicMock()
    mock_channel = MagicMock()
    mock_connection.channel.return_value = mock_channel
    mock_connection_class.return_value = mock_connection
    
    producer = RabbitMQProducer(queue='custom_queue')
    assert producer.queue == 'custom_queue'


@patch('src.producer.pika.BlockingConnection')
def test_connect_success(mock_connection_class):
    """Test successful connection."""
    mock_connection = MagicMock()
    mock_channel = MagicMock()
    mock_connection.channel.return_value = mock_channel
    mock_connection_class.return_value = mock_connection
    
    producer = RabbitMQProducer()
    producer.connect()
    
    assert producer.connection is not None
    assert producer.channel is not None


@patch('src.producer.pika.BlockingConnection')
def test_publish_message(mock_connection_class):
    """Test publishing a message."""
    mock_connection = MagicMock()
    mock_channel = MagicMock()
    mock_connection.channel.return_value = mock_channel
    mock_connection_class.return_value = mock_connection
    
    producer = RabbitMQProducer()
    producer.connect()
    
    message = {'filename': 'test.txt', 'size': 100}
    result = producer.publish_message(message)
    
    assert result is True
    mock_channel.basic_publish.assert_called_once()


@patch('src.producer.pika.BlockingConnection')
def test_close_connection(mock_connection_class):
    """Test closing connection."""
    mock_connection = MagicMock()
    mock_channel = MagicMock()
    mock_connection.channel.return_value = mock_channel
    mock_connection_class.return_value = mock_connection
    
    producer = RabbitMQProducer()
    producer.connect()
    producer.close()
    
    mock_channel.close.assert_called_once()
    mock_connection.close.assert_called_once()

