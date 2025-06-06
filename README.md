# Syslog Sidecar Application

This is a simple Python application that logs to syslog, with a Fluentd sidecar container that forwards logs to a remote syslog server.

## Prerequisites

- Docker
- Kubernetes cluster (local or remote)
- kubectl configured to work with your cluster

## Building the Application

1. Build the Python application Docker image:
```bash
docker build -t syslog-app:latest .
```

2. Build the Fluentd Docker image:
```bash
docker build -t fluentd-syslog:latest -f Dockerfile.fluentd .
```

## Deploying to Kubernetes

1. Deploy the syslog server first:
```bash
kubectl delete -f k8s-syslog-server.yaml
kubectl apply -f k8s-syslog-server.yaml
```

2. Deploy the main application:
```bash
kubectl delete -f k8s-deployment.yaml
kubectl apply -f k8s-deployment.yaml
```

3. Verify the deployment:
```bash
# Check all pods are running
kubectl get pods

# View logs from the Python application
kubectl logs -f <python-app-pod-name> -c python-app

# View logs from Fluentd
kubectl logs -f <python-app-pod-name> -c fluentd

# View logs from the syslog server
kubectl logs -f <syslog-server-pod-name>
```

## Architecture

- The Python application logs to syslog on localhost:514
- The Fluentd sidecar container listens on port 514 for syslog messages
- Fluentd forwards the logs to the syslog server
- The syslog server displays received messages in its logs

### Network Flow Diagram

```
+------------------+       +------------------+       +------------------+
|                  |       |                  |       |                  |
|  Python App      |------>|  Fluentd Sidecar |------>|  rsyslog Server  |
|  (localhost:514) |       |  (localhost:514) |       |  (UDP:515)       |
|                  |       |                  |       |                  |
+------------------+       +------------------+       +------------------+
```

You can configure `SYSLOG_HOST` and `SYSLOG_PORT` environment variables on python-app container to
either send to fluentd sidecar (using UDP on localhost port 514) or bypass fluentd and send directly
to rsyslog server (using UDP on syslog-server port 515).

## Notes

- The application uses UDP for syslog communication
- The syslog server is deployed as a separate service in the cluster
- The Fluentd configuration can be customized in the ConfigMap
- The Fluentd container includes the syslog plugin for forwarding logs
- The syslog server now uses rsyslog for robust syslog handling
