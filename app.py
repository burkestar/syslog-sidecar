import logging
import logging.handlers
import time
import os
import socket

# Configure logger
logger = logging.getLogger('myapp')
logger.setLevel(logging.INFO)

# Create SysLogHandler with Unix socket and LOG_LOCAL1 facility
syslog_handler = logging.handlers.SysLogHandler(
    address='/var/run/rsyslog/log.sock',
    facility=logging.handlers.SysLogHandler.LOG_LOCAL1
)
syslog_handler.setLevel(logging.INFO)
logger.addHandler(syslog_handler)

# Add console handler for debugging
console_handler = logging.StreamHandler()
console_handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
logger.addHandler(console_handler)

def main():
    logger.info("Starting Python application, sending logs to Unix socket")
    counter = 0
    while True:
        logger.info(f"Test info message {counter}")
        counter += 1
        time.sleep(5)

if __name__ == "__main__":
    main()
