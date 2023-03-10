# coding: utf_8

import datetime
import picamera
import RPi.GPIO as GPIO
import time


# タクトスイッチのコールバック関数
def tact_switch_callback(channel):
    global status
    if GPIO.input(PIN_TCT) == GPIO.LOW:
        if status == False:
            # 検出オン処理
            detect_on()
        else:
            # 検出オフ処理
            detect_off()
    print(f'status = {status}')


# 超音波センサーでの距離測定
def measure_distance():
    # 超音波を一旦OFFにしてから、0.0001秒間だけ出力
    GPIO.output(PIN_TRG, GPIO.LOW)
    time.sleep(0.001)
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
    return 34000 * (t_end - t_start) / 2


# 検知オン処理
def detect_on():
    # 検知状態をオンに変更
    global status
    status = True
    # LEDを点灯する
    GPIO.output(PIN_LED, GPIO.HIGH)
    # 静止画を撮影する
    now = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
    camera.capture(f'/home/pi/Pictures/capture_{now}.jpg')
    # 動画の撮影を開始する
    camera.start_preview(alpha=200)
    camera.start_recording(f'/home/pi/Pictures/vido_{now}.h264')


# 検知オフ処理
def detect_off():
    # 検知状態をオフに変更
    global status
    status = False
    # 動画の撮影を停止する
    camera.stop_preview()
    camera.stop_recording()
    # LEDオフ
    GPIO.output(PIN_LED, GPIO.LOW)



# 検知の閾値
THRESHOLD = 30

# 検知状態フラグ
status = False

# GPIOの設定
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# LEDの設定
PIN_LED = 4
GPIO.setup(PIN_LED, GPIO.OUT)

# タクトスイッチの設定
PIN_TCT = 21
GPIO.setup(PIN_TCT, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.add_event_detect(PIN_TCT, GPIO.BOTH, bouncetime=10,
                      callback=tact_switch_callback)
 
# カメラモジュールの設定
camera = picamera.PiCamera()
camera.resolution = (720, 480)
    
# 無限ループ
while True:
    # 待機
    time.sleep(0.1)

# GPIOの解放
GPIO.cleanup()
