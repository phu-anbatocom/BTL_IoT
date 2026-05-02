# 🛡️ Mô phỏng & Đánh giá Bảo mật IoT (Giao thức MQTT)

Đây là mã nguồn phục vụ cho Bài tập lớn môn học, tập trung vào việc nghiên cứu, mô phỏng các lỗ hổng bảo mật trên thiết bị IoT (sử dụng giao thức MQTT) và triển khai các biện pháp đối phó mã nguồn mở nhằm bảo vệ toàn vẹn dữ liệu và hệ thống.

## 📂 Cấu trúc thư mục

Dự án được chia thành 3 kịch bản chính:

```text
├── attack_script/      # Các kịch bản tấn công mạng IoT
│   ├── hacker_dos.py     # Tấn công Từ chối dịch vụ (DDoS)
│   └── hacker_inject.py  # Tấn công mạo danh / Chèn tin nhắn giả
├── basic_app/          # Kịch bản 1: Hệ thống IoT MẶC ĐỊNH (Không bảo mật)
│   ├── app.py            # Giả lập ứng dụng di động nhận dữ liệu
│   ├── mosquitto.conf    # Cấu hình MQTT Broker mở cổng 1883 (Plaintext)
│   └── sensor.py         # Giả lập cảm biến nhiệt độ gửi dữ liệu
└── secured_app/        # Kịch bản 2: Hệ thống IoT ĐÃ BẢO MẬT
    ├── app.py            # Ứng dụng nâng cấp có tích hợp TLS và Password
    ├── sensor.py         # Cảm biến nâng cấp có tích hợp TLS và Password
    ├── mosquitto.conf    # Cấu hình Broker bảo mật (Cổng 8883, User: root)
    └── (Các file chứng chỉ & mật khẩu được tự động tạo - xem hướng dẫn bên dưới)
⚙️ Yêu cầu hệ thống
Docker Desktop: Dùng để chạy máy chủ trung tâm (MQTT Broker - Eclipse Mosquitto).
Python 3.x: Chạy các script mô phỏng thiết bị.
OpenSSL: Dùng để khởi tạo chứng chỉ số (Có sẵn trên Linux/Mac/Git Bash).
Wireshark: (Tùy chọn) Để bắt gói tin mạng, kiểm chứng tính năng mã hóa TLS.
🛠️ Hướng dẫn cài đặt & Chạy kịch bản 1 (Không bảo mật)
1. Clone mã nguồn & Cài thư viện:
code
Bash
git clone https://github.com/phu-anbatocom/BTL_IoT.git
cd <tên-thư-mục-repo>
python -m venv .venv
.venv\Scripts\activate      # Môi trường Windows
# source .venv/bin/activate # Môi trường Linux/Mac
pip install paho-mqtt==1.6.1 psutil
2. Khởi động hệ thống yếu kém:
Mở terminal, di chuyển vào thư mục basic_app và khởi động Broker:
code
Bash
cd basic_app
docker run -it --name mqtt-broker -p 1883:1883 -v "%cd%:/mosquitto/config" eclipse-mosquitto
Mở 2 terminal mới (nhớ activate .venv), chạy thiết bị:
python app.py
python sensor.py
3. Thử nghiệm Tấn công:
Chạy các file trong attack_script. Bạn sẽ thấy Hacker dễ dàng chèn dữ liệu giả và đánh sập Broker. Dùng Wireshark (card Loopback) bắt cổng 1883 sẽ thấy dữ liệu dưới dạng Plaintext.
🛡️ Hướng dẫn Kịch bản 2 (Triển khai Bảo mật)
⚠️ LƯU Ý QUAN TRỌNG: Vì lý do an toàn thông tin, các file nhạy cảm (.crt, .key, passwd.txt) đã bị loại bỏ khỏi GitHub thông qua .gitignore. Bạn cần tự tạo lại chúng trước khi chạy.
Bước A: Khởi tạo dữ liệu bảo mật
Mở Terminal, di chuyển vào thư mục secured_app:
code
Bash
cd secured_app
1. Tạo file mật khẩu (Tài khoản: admin / Mật khẩu: 123456):
code
Bash
docker run --rm -v "%cd%:/mosquitto/config" eclipse-mosquitto mosquitto_passwd -c -b /mosquitto/config/passwd.txt admin 123456
2. Tạo Chứng chỉ SSL/TLS bằng OpenSSL:
(Chạy lần lượt 3 lệnh dưới đây)
code
Bash
openssl req -new -x509 -days 365 -keyout ca.key -out ca.crt -subj "/CN=My_CA" -nodes
openssl genrsa -out server.key 2048
openssl req -new -out server.csr -key server.key -subj "/CN=localhost"
openssl x509 -req -in server.csr -CA ca.crt -CAkey ca.key -CAcreateserial -out server.crt -days 365
Bước B: Khởi động hệ thống an toàn
Tắt Broker cũ đang chạy (nếu có): docker rm -f mqtt-broker.
Vẫn ở trong thư mục secured_app, chạy Broker mới:
code
Bash
docker run -it --name mqtt-broker -p 8883:8883 -p 1883:1883 -v "%cd%:/mosquitto/config" eclipse-mosquitto
Mở 2 terminal mới, chạy thiết bị:
python app.py
python sensor.py
Bước C: Nghiệm thu
Tấn công thất bại: Chạy lại attack_script, các gói tin tấn công sẽ bị Broker từ chối hoàn toàn do không có tài khoản xác thực.
Bảo mật đường truyền: Dùng Wireshark bắt cổng 8883, gói tin đã chuyển thành TLSv1.2, nội dung Payload bị mã hóa thành Encrypted Application Data.
👥 Nhóm thực hiện
Thành viên 1 - [MSSV]
Thành viên 2 - [MSSV]
