from flask import Flask, jsonify
import psycopg2

app = Flask(__name__)

# database connection helper
def get_connection():
	return psycopg2.connect(
		dbname = "oculus_db",
		user = "oculus_user",
		password = "qwertyuiop",
		host = "localhost",
		port = "5432")


# endpoint: latest metrics
@app.route("/metrics",methods=["GET"])

def get_metrices():
	try:
		conn = get_connection()
		cur = conn.cursor()

		cur.execute("""
		SELECT timestamp, cpu_percent, memory_percent, disk_io, failed_ssh
		FROM system_metrics
		ORDER BY timestamp DESC
		LIMIT 10""")
	
		rows = cur.fetchall()
		

		data = []
		for r in rows:
			data.append({
				"timestamp": r[0],
				"cpu_percent": r[1],
				"memory_percent": r[2],
				"disk_io": r[3],
				"failed_ssh": r[4]})

		cur.close()
		conn.close()
		return jsonify(data)

	except Exception as e:
		return jsonify({"error": str(e)})

# running api
if __name__ == "__main__":
	app.run(host="0.0.0.0", port=5000, debug=True)
