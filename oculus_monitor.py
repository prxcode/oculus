# importing some pkg

import psutil # for system metrics
import time # for sleeping between cycles
import os # for checking log file
from datetime import datetime
from db import insert_metrics

# to get system metrics
def get_system_metrics():
	cpu = psutil.cpu_percent(interval=1)
	memory = psutil.virtual_memory().percent
	disk = psutil.disk_io_counters()
	
	metrics = {
		"cpu_percent": cpu,
		"memory_percent": memory,
		"disk_io": {
			"read_bytes": disk.read_bytes,
			"write_bytes": disk.write_bytes,
			"read_count": disk.read_count,
			"write_count": disk.write_count

		}
	}
	return metrics # dictionary with cpu, memory and disk io stats


# to count failed ssh logins
def get_failed_ssh_attempts(log_file = "/var/log/auth.log"):
	failed_count = 0
	if not os.path.exists(log_file):
		print(f"[WARNING!] Log file {log_file} does not exist.") # if path doesn't exist 
		return failed_count

	try:
		with open(log_file, "r") as fp:
			for line in fp:
				if "failed password" in line.lower():
					failed_count += 1 # incrementing failure count for every ssh login attempt
	except PermissionError:
		print(f"[WARNING!] Permission denied for {log_file}. Try running with sudo.") # permission error
	except Exception as e:
		print(f"[ERROR] Unexpected error reading {log_file}: {e}") # for any other error 
	return failed_count

# to monitor single cycle
def monitor_cycle():
	timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S") # date and time
	metrics = get_system_metrics()
	failed_ssh = get_failed_ssh_attempts()

	insert_metrics(metrics, failed_ssh)
	print("Metrics saved to database!")

	print(f"\n[{timestamp}] Oculus Monitoring Cycle")
	print(f"CPU Usage: {metrics['cpu_percent']}%")
	print(f"Memory Usage: {metrics['memory_percent']}%")
	print(f"Disk I/O: {metrics['disk_io']}")
	print(f"Failed SSH Logins: {failed_ssh}")




# main loop for every min
def main():
	print("Starting Oculus Monitor...")
	try:
		while True:
			monitor_cycle()
			time.sleep(60) # wait for 60sec
	except KeyboardInterrupt:
		print("\nOculus Monitor Stopped...")

if __name__ == "__main__":
	main()
