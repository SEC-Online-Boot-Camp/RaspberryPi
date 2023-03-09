# coding: utf_8

import RPi.GPIO as GPIO
import time

# GPIOの設定
GPIO.setmode(GPIO.BCM)
PIN_LED = 4
GPIO.setup(PIN_LED, GPIO.OUT)

# 10回繰り返し
for _ in range(10):
    GPIO.output(PIN_LED, GPIO.HIGH)
    time.sleep(0.5)
    GPIO.output(PIN_LED, GPIO.LOW)
    time.sleep(0.5)

# GPIOの解放
GPIO.cleanup()
