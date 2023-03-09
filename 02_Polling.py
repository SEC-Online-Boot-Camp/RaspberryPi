# coding: utf_8

import RPi.GPIO as GPIO
import time

# GPIOの設定
GPIO.setmode(GPIO.BCM)
PIN_LED = 4
GPIO.setup(PIN_LED, GPIO.OUT)
PIN_TCT = 21
GPIO.setup(PIN_TCT, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

# 無限ループ
while True:
    if GPIO.input(PIN_TCT) == GPIO.HIGH:
        # タクトスイッチONの場合
        GPIO.output(PIN_LED, GPIO.HIGH)
    else:
        # タクトスイッチOFFの場合
        GPIO.output(PIN_LED, GPIO.LOW)
    time.sleep(0.1)

# GPIOの解放
GPIO.cleanup()
