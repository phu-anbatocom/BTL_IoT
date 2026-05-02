import paho.mqtt.client as mqtt
import ssl
import time
import json
import random

# Cấu hình
BROKER = "localhost"
PORT = 8883 
TOPIC = "iot/home/sensor1"

client = mqtt.Client("Sensor_Temp")

# 1. Khai báo Username / Password
client.username_pw_set("admin", "123456")

# 2. Khai báo file Chứng chỉ mã hóa (ca.crt)
client.tls_set(
    ca_certs="ca.crt", 
    tls_version=ssl.PROTOCOL_TLSv1_2
)
client.tls_insecure_set(True)

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
        time.sleep(5) # Cứ 5 giây gửi 1 lần
except KeyboardInterrupt:
    client.publish(TOPIC, json.dumps({"nhiet_do": temp, "trang_thai": "Tắt cảm biến"})) # Gửi trạng thái tắt
    print("Đã tắt cảm biến.")
    client.disconnect()