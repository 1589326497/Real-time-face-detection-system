# 实时人脸检测系统：ESP32 与上位机通信

在这篇博客中，我将介绍如何使用 ESP32 摄像头捕获图像，并通过 UDP 协议将图像传输到上位机进行实时人脸检测。我们将使用 Python 编程语言和 OpenCV 库来实现上位机端的人脸检测功能。

**效果如下**
![IMG20240528233141](https://github.com/1589326497/Real-time-face-detection-system/assets/113960039/f5692831-4203-4ab2-90cf-aa4209c08c87)
![image](https://github.com/1589326497/Real-time-face-detection-system/assets/113960039/6aba8e2c-e434-4d4e-a744-6dadd6ad44f8)







## 硬件与软件准备

1. **ESP32 开发板**：我们使用 ESP32 开发板和摄像头模块来捕获图像。
2. **上位机**：需要一台装有 Python 和 OpenCV 库的计算机作为上位机。
3. **WiFi 网络**：确保 ESP32 和上位机连接到同一 WiFi 网络，以便它们之间能够进行通信。

## ESP32 代码解析

在 ESP32 的代码中，我们首先初始化摄像头，并设置一些参数，如分辨率、特效、白平衡等。然后，我们创建一个 UDP socket，并持续地捕获图像并通过 UDP 发送到指定的 IP 地址和端口。下面是代码的关键部分：

```python
# 连接wifi
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
if not wlan.isconnected():
    print('连接到网络...')
    wlan.connect('wifi账号', 'wifi密码')
    
    while not wlan.isconnected():
        pass
print('网络配置:', wlan.ifconfig())

# 摄像头初始化
try:
    camera.init(0, format=camera.JPEG)
except Exception as e:
    camera.deinit()
    camera.init(0, format=camera.JPEG)

# 创建 UDP socket
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, 0)

# 捕获图像并发送到指定地址
while True:
    buf = camera.capture()
    s.sendto(buf, ("192.168.3.5", 9090))
    time.sleep(0.1)
```

## 上位机代码解析

在上位机的代码中，我们创建一个 UDP socket，并监听指定端口。当收到来自 ESP32 的图像数据时，我们将其转换为 OpenCV 图像格式，并使用 Haar 特征级联分类器检测图像中的人脸。最后，我们在图像中绘制矩形框来标记检测到的人脸。下面是代码的关键部分：

```python
# 加载用于人脸检测的预训练 Haar 特征级联分类器
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# 创建 UDP socket 并绑定端口
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, 0)
s.bind(("0.0.0.0", 9090))

# 接收并处理来自 ESP32 的图像数据
while True:
    data, IP = s.recvfrom(100000)
    bytes_stream = io.BytesIO(data)
    image = Image.open(bytes_stream)
    img = np.asarray(image)
    img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

    # 在图像中检测人脸
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

    # 绘制矩形框标记人脸
    for (x, y, w, h) in faces:
        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 2)

    cv2.imshow("ESP32 捕获的图像", img)
    if cv2.waitKey(1) == ord("q"):
        break

s.close()
cv2.destroyAllWindows()
```

## 结论

一个简单的实时人脸检测系统，利用 ESP32 捕获图像并通过 WiFi 发送到上位机，然后在上位机中使用 OpenCV 对图像进行处理并实时显示人脸检测结果。

