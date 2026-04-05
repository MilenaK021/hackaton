from flask import Flask, request, jsonify
import csv
from datetime import datetime
import os

app = Flask(__name__)

CSV_FILE = "locomotive_data.csv"
HEADERS = ["timestamp", "system_id", "temperature", "pressure", "speed", "vibration"]

if not os.path.exists(CSV_FILE):
    with open(CSV_FILE, mode='w', newline='', encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(HEADERS)

@app.route('/data', methods=['POST'])
def receive_data():
    data = request.json

    row = [
        datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        data.get("system_id"),
        data.get("temperature"),
        data.get("pressure"),
        data.get("speed"),
        data.get("vibration")
    ]

    with open(CSV_FILE, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(row)

    return jsonify({"status": "ok"}), 200

if __name__ == "__main__":
    app.run(debug=True)