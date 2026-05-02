import paho.mqtt.client as mqtt
import ssl

BROKER = "localhost"
PORT = 8883
TOPIC = "iot/home/sensor1"

client = mqtt.Client("Mobile_App")

# 1. Khai báo Username / Password
client.username_pw_set("admin", "123456")

# 2. Khai báo file Chứng chỉ mã hóa (ca.crt)
client.tls_set(
    ca_certs="ca.crt", 
    tls_version=ssl.PROTOCOL_TLSv1_2
)
client.tls_insecure_set(True)

# Hàm chạy khi nhận được dữ liệu
def on_message(client, userdata, msg):
    print(f"App nhận được cảnh báo: Topic={msg.topic} | Dữ liệu={msg.payload.decode()}")

client.on_message = on_message

client.connect(BROKER, PORT)
client.subscribe(TOPIC) # Lắng nghe dữ liệu (Subscribe)

print("App đang lắng nghe dữ liệu từ cảm biến...")
client.loop_forever()