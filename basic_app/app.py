import paho.mqtt.client as mqtt

BROKER = "127.0.0.1"
PORT = 1883
TOPIC = "iot/home/sensor1"

# Hàm chạy khi nhận được dữ liệu
def on_message(client, userdata, msg):
    print(f"App nhận được cảnh báo: Topic={msg.topic} | Dữ liệu={msg.payload.decode()}")

client = mqtt.Client("Mobile_App")
client.on_message = on_message

client.connect(BROKER, PORT)
client.subscribe(TOPIC) # Lắng nghe dữ liệu (Subscribe)

print("App đang lắng nghe dữ liệu từ cảm biến...")
client.loop_forever()