

"""
Main entry point for the RabbitMQ file scanner.
Recursively scans a directory and sends file information to RabbitMQ.
"""

import argparse
import sys
from pathlib import Path

from src.file_scanner import FileScanner
from src.producer import RabbitMQProducer
from config import DEFAULT_QUEUE


def main():
    """Main function to run the file scanner."""

    parser = argparse.ArgumentParser(
        description='Recursively scan a directory and send file information to RabbitMQ'
    )
    parser.add_argument('directory', type=str, help='Root directory to scan')
    parser.add_argument('--queue', type=str, default=DEFAULT_QUEUE,
                        help=f'RabbitMQ queue name (default: {DEFAULT_QUEUE})')
    parser.add_argument('--follow-symlinks', action='store_true',
                        help='Follow symbolic links')

    args = parser.parse_args()
    directory = Path(args.directory).expanduser().resolve()

    if not directory.exists() or not directory.is_dir():
        directory = Path(args.directory).expanduser().resolve()
        if not directory.exists() or not directory.is_dir():
            print(
                f"Error: Directory does not exist: {directory}", file=sys.stderr)
            sys.exit(1)

    scanner = FileScanner(str(directory), follow_symlinks=args.follow_symlinks)
    producer = RabbitMQProducer(queue=args.queue)

    try:
        print(f"Connecting to RabbitMQ...")
        producer.connect()
        print(f"Scanning directory: {directory}")
        print(f"Sending messages to queue: {args.queue}")

        messages_sent = 0
        for file_info in scanner.scan():
            if producer.publish_message(file_info):
                messages_sent += 1
            else:
                print(
                    f"Failed to send message for: {file_info['filename']}", file=sys.stderr)

        print(f"\nScan complete. Messages sent: {messages_sent}")
        producer.close()

    except KeyboardInterrupt:
        print("\nScan interrupted by user")
        producer.close()
        sys.exit(0)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        producer.close()
        sys.exit(1)


if __name__ == '__main__':
    main()
