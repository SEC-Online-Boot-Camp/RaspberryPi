# coding: utf_8

import datetime
import picamera
import RPi.GPIO as GPIO
import time

from keras.models import load_model  # TensorFlow is required for Keras to work
from PIL import Image, ImageOps  # Install pillow instead of PIL
import numpy as np

#
def classify_picture(image_path):
    # Disable scientific notation for clarity
    np.set_printoptions(suppress=True)

    # Load the model
    model = load_model("/home/pi/Downloads/keras_model.h5", compile=False)

    # Load the labels
    class_names = open("/home/pi/Downloads/labels.txt", "r").readlines()

    # Create the array of the right shape to feed into the keras model
    # The 'length' or number of images you can put into the array is
    # determined by the first position in the shape tuple, in this case 1
    data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)

    # Replace this with the path to your image
    image = Image.open(image_path).convert("RGB")

    # resizing the image to be at least 224x224 and then cropping from the center
    size = (224, 224)
    image = ImageOps.fit(image, size, Image.Resampling.LANCZOS)

    # turn the image into a numpy array
    image_array = np.asarray(image)

    # Normalize the image
    normalized_image_array = (image_array.astype(np.float32) / 127.5) - 1

    # Load the image into the array
    data[0] = normalized_image_array

    # Predicts the model
    prediction = model.predict(data)
    index = np.argmax(prediction)
    class_name = class_names[index]
    confidence_score = prediction[0][index]

    # Print prediction and confidence score
    return class_name[2:], confidence_score



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
 
# 超音波センサーの設定
PIN_TRG = 5
PIN_ECH = 13
GPIO.setup(PIN_TRG, GPIO.OUT)
GPIO.setup(PIN_ECH, GPIO.IN)

# カメラモジュールの設定
camera = picamera.PiCamera()
camera.resolution = (720, 480)
    
# 無限ループ
while True:
    # 超音波センサーで距離を測定
    d = measure_distance()
    print(f'distance = {d}')

    # 物体検知判定
    if status == False and d <= THRESHOLD:
        # 検知オフ状態で、物体が近づいた場合
        # 静止画を撮影する
        now = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
        image_path = f'/home/pi/Pictures/capture_{now}.jpg'
        camera.capture(image_path)
        # 画像を判定する
        label, score = classify_picture(image_path)
        print(label, score)
        # 人間の場合のみ、検知オン処理
        if label == '人間' and score > 80:
             detect_on()
    elif status == True and d > THRESHOLD:
        # 検知オン状態で、物体が離れた場合
        detect_off()
       
    # 待機
    time.sleep(0.1)

# GPIOの解放
GPIO.cleanup()
