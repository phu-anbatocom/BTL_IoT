import paho.mqtt.client as mqtt
import time
import json
import random

# Cấu hình
BROKER = "127.0.0.1"
PORT = 1883
TOPIC = "iot/home/sensor1"

client = mqtt.Client("Sensor_Temp")
client.connect(BROKER, PORT)

print("Cảm biến đã bật. Đang gửi dữ liệu...")
try:
    while True:
        # Tạo dữ liệu giả
        temp = random.randint(20, 35)
        payload = json.dumps({"nhiet_do": temp, "trang_thai": "Binh thuong"})
        
        # Gửi dữ liệu (Publish)
        client.publish(TOPIC, payload)
        print(f"Đã gửi: {payload}")
        time.sleep(3) # Cứ 3 giây gửi 1 lần
except KeyboardInterrupt:
    print("Đã tắt cảm biến.")
    client.disconnect()