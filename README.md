# RabbitMQ File Scanner

A Python application that recursively scans a local directory and sends file information to a RabbitMQ queue. Each file found is published as a JSON message containing file metadata (path, filename, size, etc.).

## Overview

This project implements a robust file system scanner that integrates with RabbitMQ for asynchronous message processing. Built with Python and the Pika library, it provides a scalable and simple solution for processing large directory structures and distributing file metadata through message queues.

### Key Features

- **Recursive Directory Scanning**: Traverses directory trees efficiently to check files
- **RabbitMQ Integration**: Publishes file metadata as JSON messages
- **Error Handling**: Gracefully handles permission errors and connection issues
- **Configurable**: Easy-to-modify connection settings
- **Test Coverage**: Comprehensive test suite for reliability 

## Installation

### Prerequisites

- Python 3.7 or higher
- Docker and Docker Compose (for RabbitMQ)

### Setup Steps

1. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Activate virtual environment:**
   ```bash
   source .venv/bin/activate
   ```

3. **Start RabbitMQ using Docker Compose:**
   ```bash
   docker compose up -d
   ```

   This will start RabbitMQ with:
   - AMQP port: `5672` (for application connections)
   - Management UI: `http://localhost:15672` (web interface)

## Usage

### Running the Verifier

```bash
python verify_consumer.py
```


### Running the File Scanner

Scan a directory and send file information to RabbitMQ:

```bash
python3 main.py tests
```

**Command-line Options:**
- `--queue QUEUE` - Specify RabbitMQ queue name (default: `norcom_queue`)
- `--follow-symlinks` - Follow symbolic links during scanning

**Examples:**
```bash
# Scan current directory
python main.py .

# Scan with custom queue name
python main.py /home/user/documents --queue my_files_queue

# Scan and follow symbolic links
python main.py /path/to/dir --follow-symlinks
```

### Verifying Messages

Use the verification consumer to view messages in the queue and confirm that the essential connection to the message broker is working correctly:

```bash
python verify_consumer.py
```


## Configuration

### Connection Settings

The application uses default RabbitMQ settings. Modify `config.py` to change connection parameters:

```python
RABBITMQ_HOST = 'localhost'
RABBITMQ_PORT = 5672
RABBITMQ_USERNAME = 'guest'
RABBITMQ_PASSWORD = 'guest'
RABBITMQ_VIRTUAL_HOST = '/'

DEFAULT_QUEUE = 'norcom_queue'
DEFAULT_EXCHANGE = 'norcom_exchange'
DEFAULT_ROUTING_KEY = 'norcom.routing.key'
```

### Required Parameters

- **Directory path**: The root directory to scan (required positional argument)

## How to Check Messages in RabbitMQ


### Method:


1. Open `http://localhost:15672` in your browser
2. Login with credentials:
   - Default: `guest`/`guest`
   - Docker: `admin`/`admin` (if configured)
3. Navigate to the **Queues** tab
4. Select your queue name (e.g., `norcom_queue`) and check the state
5. Click **Get messages** to view queued messages


## Message Format

Each file generates a JSON message with the following structure:

```json
{
  "filename": "example.txt",
  "path": "/absolute/path/to/example.txt",
  "relative_path": "subdir/example.txt",
  "size": 1024
}
```

**Fields:**
- `filename` - Name of the file
- `path` - Absolute path to the file
- `relative_path` - Path relative to scanned directory
- `size` - File size in bytes

## Project Structure

```

NorCom_RabbitMQ/
├── .gitignore
├── config.py                  # Configuration settings
├── docker-compose.yaml        # Run docker
├── main.py                    # Main program entry point
├── requirements.txt           # Python dependencies
├── verify_consumer.py         # Simple consumer for message verification   
│
├── src/                       # Application source code
│   ├── __init__.py            # Marks src as a package
│   ├── file_scanner.py        # Recursive filesystem scanning logic
│   └── producer.py            # RabbitMQ message producer
│
└── tests/                     # Unit tests
    ├── __init__.py            # Marks tests as a package
    ├── test_file_scanner.py   # Tests for file_scanner module
    └── test_producer.py       # Tests for producer module


```

## Testing

Run the test suite:

```bash
pytest tests/
```

Run with verbose output:

```bash
pytest tests/ -v
```

## Troubleshooting

### Connection Issues

If you encounter connection errors:
- Ensure RabbitMQ is running: `docker ps`
- Check that ports 5672 and 15672 are not already in use
- Verify connection settings in `config.py`



## References
* GitHub RabbitMQ (Messaging Broker): https://github.com/rabbitmq


### Permission Errors

The scanner will skip files and directories it cannot access, logging warnings for inaccessible paths.

## License

MIT License
