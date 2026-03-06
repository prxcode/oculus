## Oculus Infrastructure Monitoring Daemon
- It will run continuously in the background, every 60 sec.
- Collects system metrics:
	- CPU usage
	- Memory Usage
	- Disk I/O
- Parse system logs to detect, failed SSH login attempts
- Send data to PostgreSQL, expose small API to visualize metrices

## Features
- CPU, memory, disk monitoring
- SSH attack detection
- PostgreSQL telemetry storage
- systemd daemon
- REST API for metrics

## Setup
- Install dependencies: `pip install -r requirements.txt`
- Start monitoring daemon: `systemctl start oculus`
- Start API: `python api.py`
- Run Oculus: `python oculus_monitoring.py`
