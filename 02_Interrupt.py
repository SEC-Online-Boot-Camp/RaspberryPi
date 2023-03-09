# coding: utf_8

import RPi.GPIO as GPIO
import time

# コールバック関数の定義
def tact_switch_callback(channel):
    if GPIO.input(PIN_TCT) == GPIO.HIGH:
        GPIO.output(PIN_LED, GPIO.HIGH)
    else:
        GPIO.output(PIN_LED, GPIO.LOW)

# GPIOの設定
GPIO.setmode(GPIO.BCM)
PIN_LED = 4                                                                                                                                                                           
GPIO.setup(PIN_LED, GPIO.OUT)
PIN_TCT = 21
GPIO.setup(PIN_TCT, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.add_event_detect(PIN_TCT, GPIO.BOTH, bouncetime=100,
                      callback=tact_switch_callback)

# 無限ループ
while True:
    time.sleep(0.01)

# GPIOの解放
GPIO.cleanup()
