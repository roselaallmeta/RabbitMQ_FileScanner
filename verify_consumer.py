"""
Simple consumer script to verify messages in RabbitMQ queue.
"""
import json
import pika
import sys
from argparse import ArgumentParser
from config import (
    RABBITMQ_HOST,
    RABBITMQ_PORT,
    RABBITMQ_USERNAME,
    RABBITMQ_PASSWORD,
    RABBITMQ_VIRTUAL_HOST,
    DEFAULT_QUEUE
)


def main():
    """Main function to consume and display messages."""
    parser = ArgumentParser(description='Consume messages from RabbitMQ queue')
    parser.add_argument('--queue', type=str, default=DEFAULT_QUEUE,
                       help=f'Queue name (default: {DEFAULT_QUEUE})')
    parser.add_argument('--count', '-c', type=int,
                       help='Number of messages to consume')
    parser.add_argument('--verbose', '-v', action='store_true',
                       help='Show full JSON details')
    
    args = parser.parse_args()
    
    try:
        
        credentials = pika.PlainCredentials(RABBITMQ_USERNAME, RABBITMQ_PASSWORD)
        parameters = pika.ConnectionParameters(
            host=RABBITMQ_HOST,
            port=RABBITMQ_PORT,
            virtual_host=RABBITMQ_VIRTUAL_HOST,
            credentials=credentials
        )
        
        connection = pika.BlockingConnection(parameters)
        channel = connection.channel()
        channel.queue_declare(queue=args.queue, durable=True)
        
        print(f"Connected to RabbitMQ. Queue: {args.queue}")
        print("Press CTRL+C to exit\n")
        
        messages_received = 0
        
        def callback(ch, method, properties, body):
            nonlocal messages_received
            messages_received += 1
            
            message = json.loads(body)
            
            if args.verbose:
                print(f"\n--- Message #{messages_received} ---")
                print(json.dumps(message, indent=2))
            else:
                filename = message.get('filename', 'unknown')
                size = message.get('size_human', 'unknown')
                path = message.get('relative_path', 'unknown')
                print(f"[{messages_received}] {filename} ({size}) - {path}")
            
            ch.basic_ack(delivery_tag=method.delivery_tag)
            
            if args.count and messages_received >= args.count:
                ch.stop_consuming()
        
        channel.basic_qos(prefetch_count=1)
        channel.basic_consume(queue=args.queue, on_message_callback=callback)
        channel.start_consuming()
        
    except KeyboardInterrupt:
        print(f"\nStopped. Total messages received: {messages_received}")
        if 'channel' in locals():
            channel.stop_consuming()
        if 'connection' in locals():
            connection.close()
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()

