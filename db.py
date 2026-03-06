# importing libraries

import psycopg2
import json


# insert monitoring metrics into postgresql
def insert_metrics(metrics, failed_ssh):
	try:
		conn = psycopg2.connect(
			dbname = "oculus_db",
			user = "oculus_user",
			password = "qwertyuiop",
			host = "localhost",
			port = "5432")
		cur = conn.cursor() 
		
		# sql insert query
		query = """
		INSERT INTO system_metrics
		(timestamp, cpu_percent, memory_percent, disk_io, failed_ssh)
		VALUES (NOW(), %s, %s, %s, %s)
		"""

		# execute query with values
		cur.execute(query, (
			metrics["cpu_percent"],
			metrics["memory_percent"],
			json.dumps(metrics["disk_io"]),
			failed_ssh))

		conn.commit()
		cur.close()
		conn.close()

	except Exception as e:
		print("Database insert error: ",e)
