import socket
import cv2
import io
from PIL import Image
import numpy as np

# 加载用于人脸检测的预训练 Haar 特征级联分类器
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, 0)
s.bind(("0.0.0.0", 9090))

while True:
    data, IP = s.recvfrom(100000)
    bytes_stream = io.BytesIO(data)
    image = Image.open(bytes_stream)
    img = np.asarray(image)
    img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)  # ESP32 采集的是 RGB 格式，要转换为 BGR（opencv 的格式）

    # 将图像转换为灰度图以进行人脸检测
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # 在图像中检测人脸
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

    # 在检测到的人脸周围画矩形框
    for (x, y, w, h) in faces:
        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 2)

    cv2.imshow("ESP32 捕获的图像", img)
    if cv2.waitKey(1) == ord("q"):
        break

s.close()
cv2.destroyAllWindows()
