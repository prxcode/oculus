# Oculus – A Simple Linux Infrastructure Monitoring Daemon
Oculus is a small infrastructure monitoring project I built to understand how monitoring tools interact with the Linux operating system.
Instead of using an existing monitoring platform, I wanted to build a basic monitoring stack from scratch. Oculus collects system metrics, looks for failed SSH login attempts, stores everything in PostgreSQL, and exposes the data through a simple API.
The project is meant to be lightweight, educational, and easy to run locally.

---

## What Oculus Does
Oculus runs continuously in the background and every 60 seconds it:
- Collects system metrics (CPU, memory, disk I/O)
- Parses system logs to detect failed SSH login attempts
- Stores the collected data in PostgreSQL
- Makes the data available through a small API
The idea is to simulate the basic workflow of a monitoring tool.
---

## Features
- CPU usage monitoring
- Memory usage tracking
- Disk I/O monitoring
- Detection of failed SSH login attempts
- PostgreSQL telemetry storage
- Simple REST API for accessing metrics
- Can run as a background service using systemd
---

## Project Structure
```
oculus/
│
├── oculus_monitoring.py
├── api.py
├── requirements.txt
├── README.md
└── systemd/
    └── oculus.service
```

**Main files**
- `oculus_monitoring.py`  
  The main monitoring script that collects metrics and sends them to the database.
- `api.py`  
  A small Flask API used to query stored metrics.
- `systemd/oculus.service`  
  Service configuration for running Oculus as a system daemon.
---

## Metrics Collected
Right now Oculus collects:
- CPU usage percentage
- Memory usage percentage
- Disk I/O statistics
- Number of failed SSH login attempts
Metrics are collected every **60 seconds**.

---

## Database Schema
Metrics are stored in a simple PostgreSQL table:
```sql
CREATE TABLE system_metrics (
    timestamp TIMESTAMP,
    cpu_percent FLOAT,
    memory_percent FLOAT,
    disk_io JSONB,
    failed_ssh INT
);
```

This keeps things flexible while still allowing basic analysis later.

---
## Installation
### 1. Clone the repository
```bash
git clone https://github.com/prxcode/oculus.git
cd oculus
```
---
### 2. Create a virtual environment (optional but recommended
```bash
python3 -m venv venv
source venv/bin/activate
```
---
### 3. Install dependencies
```bash
pip install -r requirements.txt
```
---
### 4. Set up PostgreSQL
Create a database and the metrics table.
Example:
```sql
CREATE DATABASE oculus;
```
Then create the metrics table:
```sql
CREATE TABLE system_metrics (
    timestamp TIMESTAMP,
    cpu_percent FLOAT,
    memory_percent FLOAT,
    disk_io JSONB,
    failed_ssh INT
);
```
Update the database connection details in the project if necessary.
---
## Running the Monitor
You can run the monitoring script directly:
```bash
python oculus_monitoring.py
```
Once running, the script will collect metrics and push them to PostgreSQL every 60 seconds.
---
## Running the API
Start the API server with:
```bash
python api.py
```
By default the API runs on:
```
http://127.0.0.1:5000
```
Example endpoint:
```
GET /metrics
```
This returns stored metrics in JSON format.
---
## Running Oculus as a systemd Service
If you want Oculus to run automatically in the background:
Copy the service file:
```bash
sudo cp systemd/oculus.service /etc/systemd/system/
```

Reload systemd:
```bash
sudo systemctl daemon-reload
```

Enable the service at boot:
```bash
sudo systemctl enable oculus
```

Start the service:
```bash
sudo systemctl start oculus
```

Check service status:

```bash
systemctl status oculus
```

View logs:
```bash
journalctl -u oculus
```

---

## How SSH Failures Are Detected
Oculus scans the authentication log:
```
/var/log/auth.log
```

It looks for entries like:
```
Failed password for invalid user
Failed password for root
```
This provides a basic indicator of potential SSH brute-force attempts.

---

## Why I Built This
I wanted to understand how infrastructure monitoring actually works under the hood.
Building Oculus helped me learn more about:
- collecting system telemetry
- parsing Linux logs
- integrating Python with PostgreSQL
- running background services with systemd
- exposing metrics through an API

---

## Possible Future Improvements
Some ideas for extending the project:
- simple dashboard for visualizing metrics
- alerting for suspicious SSH activity
- support for multiple monitored hosts
- containerized deployment
- integration with monitoring dashboards
