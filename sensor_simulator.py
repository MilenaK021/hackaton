import requests
import random
import time

URL = "http://127.0.0.1:5000/data"

SYSTEMS = {
    "engine": {
        "temperature": (70, 110),
        "pressure": (30, 60),
        "speed": (60, 120),
        "vibration": (0.2, 1.5)
    },
    "brakes": {
        "temperature": (40, 90),
        "pressure": (20, 50),
        "speed": (0, 80),
        "vibration": (0.1, 1.0)
    },
    "battery": {
        "temperature": (20, 50),
        "pressure": (0, 10),
        "speed": (0, 0),
        "vibration": (0.0, 0.3)
    }
}

while True:
    for system_id, ranges in SYSTEMS.items():
        payload = {
            "system_id": system_id,
            "temperature": round(random.uniform(*ranges["temperature"]), 2),
            "pressure": round(random.uniform(*ranges["pressure"]), 2),
            "speed": round(random.uniform(*ranges["speed"]), 2),
            "vibration": round(random.uniform(*ranges["vibration"]), 2)
        }

        requests.post(URL, json=payload)
        print("Sent:", payload)

    time.sleep(3)