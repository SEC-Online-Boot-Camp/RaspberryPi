# coding: utf_8

import datetime
import picamera
import RPi.GPIO as GPIO
import time


# LEDクラス
class LED:
    def __init__(self, pin1):
        self.pin1 = pin1
        GPIO.setup(pin1, GPIO.OUT)

    def control(self, on_off):
        GPIO.output(self.pin1, on_off)


# タクトスイッチクラス
class TactSwitch:
    def __init__(self, pin1):
        self.pin1 = pin1
        GPIO.setup(pin1, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
 
    def status(self):
        return GPIO.input(self.pin1)


# メイン関数
if __name__ == '__main__':
    # GPIOの設定
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)

    # インスタンス生成
    led = LED(22)
    tact_switch = TactSwitch(21)

    # カメラの設定
    camera = picamera.PiCamera()
    camera.start_preview(alpha=200)

    # 検知状態（True：検知状態、False：非検知状態）
    status = False

    # 無限ループでポーリング
    while True:
        # タクトスイッチの状態チェック
        tact_status = tact_switch.status()
        if status == False and tact_status == True:
            # 検知状態
            status = True
            # LEDオン
            led.control(True)
        if status == True and tact_status == False:
            # 非検知状態
            status = False
            # LEDオフ
            led.control(False)

        if status:
            # 検知状態なら静止画撮影
            now = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
            camera.capture(f'/home/pi/Pictures/capture_{now}.jpg')
            time.sleep(0.9)
        
        time.sleep(0.1)

    # GPIOの解放
    GPIO.cleanup()
