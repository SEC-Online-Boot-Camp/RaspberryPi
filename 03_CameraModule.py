# coding: utf_8

import datetime
import picamera
import time

# カメラの設定
camera = picamera.PiCamera()
camera.start_preview(alpha=200)

# 10回繰り返し
for _ in range(10):
    now = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
    camera.capture(f'/home/pi/Pictures/capture_{now}.jpg')
    time.sleep(1)

# カメラの終了
camera.stop_preview()
