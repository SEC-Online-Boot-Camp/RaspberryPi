# coding: utf_8

import RPi.GPIO as GPIO
import time

# GPIOの設定
GPIO.setmode(GPIO.BCM)
PIN_TRG = 5
PIN_ECH = 13
GPIO.setup(PIN_TRG, GPIO.OUT)
GPIO.setup(PIN_ECH, GPIO.IN)

# 超音波を一旦OFFにしてから、0.0001秒間だdけ出力
GPIO.output(PIN_TRG, GPIO.LOW)
time.sleep(0.1)
GPIO.output(PIN_TRG, GPIO.HIGH)
time.sleep(0.001)
GPIO.output(PIN_TRG, GPIO.LOW)

# ECHOピンがONになったら計測開始
t_start = 0
while True:
    if GPIO.input(PIN_ECH) == GPIO.HIGH:
        t_start = time.time()
        break
        
# ECHOピンがOFFになったら計測終了
t_end = 0
while True:
    if GPIO.input(PIN_ECH) == GPIO.LOW:
        t_end = time.time()
        break

# 距離 = 音速 * 到達時刻 / 2
d = 34000 * (t_end - t_start) / 2
print(f'distace = {d}\n')

# GPIOの解放
GPIO.cleanup()
