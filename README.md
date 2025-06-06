# Syslog Sidecar Example

This example demonstrates how to forward logs from a Python application to a remote syslog server using rsyslog as a sidecar container.

## Architecture

- **Python Application**: Generates logs and sends them to a Unix domain socket
- **rsyslog Sidecar**: Receives logs from the Unix domain socket and forwards them to the remote syslog server
- **Remote Syslog Server**: Receives and processes the forwarded logs

## Components

1. **Python Application (`app.py`)**
   - Uses Python's `SysLogHandler` to send logs to a Unix domain socket
   - Configured to send logs in RFC 5424 format

2. **rsyslog Sidecar**
   - Uses the official `rsyslog/syslog_appliance_alpine` image
   - Listens on a Unix domain socket for logs from the Python application
   - Forwards logs to the remote syslog server using UDP

3. **Remote Syslog Server**
   - Listens on UDP port 10515 for incoming syslog messages
   - Processes and stores the received logs

## Configuration

### rsyslog Configuration (`rsyslog.conf`)
```conf
# Load modules
module(load="imuxsock")
module(load="builtin:omfwd")

# Listen on Unix socket
input(type="imuxsock" Socket="/var/run/rsyslog/log.sock")

# Forward to syslog server
*.* action(type="omfwd"
          target="syslog-server"
          port="10515"
          protocol="udp"
          action.resumeRetryCount="10"
          queue.type="linkedList"
          queue.size="10000")
```

### Python Application Configuration
The Python application is configured to send logs to the Unix domain socket at `/var/run/rsyslog/log.sock`.

## Deployment

1. Build the Python application image:
   ```bash
   docker build -t syslog-app:latest -f Dockerfile .
   ```

2. Deploy the application and rsyslog sidecar:
   ```bash
   kubectl apply -f k8s-deployment.yaml
   ```

## Testing

1. Check if the Python application is sending logs:
   ```bash
   kubectl logs -l app=syslog-app -c python-app
   ```

2. Check if the rsyslog sidecar is forwarding logs:
   ```bash
   kubectl logs -l app=syslog-app -c rsyslog
   ```

3. Check if the remote syslog server is receiving logs:
   ```bash
   kubectl logs -l app=syslog-server
   ```

## Troubleshooting

If logs are not being forwarded:

1. Check if the Unix domain socket exists:
   ```bash
   kubectl exec -it $(kubectl get pod -l app=syslog-app -o jsonpath='{.items[0].metadata.name}') -c rsyslog -- ls -la /var/run/rsyslog/log.sock
   ```

2. Check rsyslog configuration:
   ```bash
   kubectl exec -it $(kubectl get pod -l app=syslog-app -o jsonpath='{.items[0].metadata.name}') -c rsyslog -- cat /etc/rsyslog.conf
   ```

3. Check rsyslog debug logs:
   ```bash
   kubectl exec -it $(kubectl get pod -l app=syslog-app -o jsonpath='{.items[0].metadata.name}') -c rsyslog -- cat /var/log/rsyslog-debug.log
   ```
