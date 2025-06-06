import logging
import logging.handlers
import time
import os
import socket
from datetime import datetime

class RFC5424Formatter(logging.Formatter):
    def format(self, record):
        pri = 14  # user.info
        version = 1
        timestamp = datetime.utcnow().isoformat(timespec='milliseconds') + 'Z'
        hostname = socket.gethostname()
        app_name = record.name
        procid = str(os.getpid())
        msgid = '-'
        msg = super().format(record)
        # RFC 5424: <PRI>1 TIMESTAMP HOSTNAME APP-NAME PROCID MSGID - MSG
        return f"<{pri}>{version} {timestamp} {hostname} {app_name} {procid} {msgid} - {msg}"

# Configure logger
logger = logging.getLogger('myapp')
logger.setLevel(logging.INFO)

SYSLOG_HOST = os.environ.get('SYSLOG_HOST', 'syslog-server')
SYSLOG_PORT = int(os.environ.get('SYSLOG_PORT', 10515))

# Create SysLogHandler with UDP transport
syslog_handler = logging.handlers.SysLogHandler(
    address=(SYSLOG_HOST, SYSLOG_PORT),
    facility=logging.handlers.SysLogHandler.LOG_USER,
    socktype=socket.SOCK_DGRAM
)
syslog_handler.setFormatter(RFC5424Formatter('%(message)s'))
syslog_handler.setLevel(logging.INFO)
logger.addHandler(syslog_handler)

# Add console handler for debugging
console_handler = logging.StreamHandler()
console_handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
logger.addHandler(console_handler)

def main():
    logger.info(f"Starting Python application, sending logs to {SYSLOG_HOST}:{SYSLOG_PORT}")

    counter = 0
    while True:
        # Send messages with different severity levels
        logger.info(f"Test info message {counter}")
        # Force flush the syslog handler
        syslog_handler.flush()
        counter += 1
        time.sleep(5)

if __name__ == "__main__":
    main()
