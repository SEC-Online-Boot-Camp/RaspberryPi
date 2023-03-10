# ラズパイ実習

#### バージョンの確認とPython3系への切り替え

```
# バージョンの確認
pi@raspberrypi:~ $ python --version
Python 2.7.16

# Python3系への切り替え
pi@raspberrypi:~ $ cd /usr/bin
pi@raspberrypi:~ $ sudo unlink python
pi@raspberrypi:~ $ sudo ln -s python3 python

# バージョンの確認
pi@raspberrypi:~ $ python --version
Python 3.7.3
```

### TensorFlowとKerasのインストール

#### 実行に必要なモジュールの追加

```
pi@raspberrypi:~ $ sudo apt-get install libblas-dev
pi@raspberrypi:~ $ sudo apt-get install liblapack-dev
pi@raspberrypi:~ $ sudo apt-get install python3-dev 
pi@raspberrypi:~ $ sudo apt-get install libatlas-base-dev
pi@raspberrypi:~ $ sudo apt-get install gfortran
pi@raspberrypi:~ $ sudo apt-get install python3-setuptools
pi@raspberrypi:~ $ sudo apt-get install python3-scipy
pi@raspberrypi:~ $ sudo apt-get update
pi@raspberrypi:~ $ sudo apt-get install python3-h5py
```

#### TesorFlowとKerasのインストール

```
pi@raspberrypi:~ $ pip install --upgrade scipy
pi@raspberrypi:~ $ pip install --upgrade cython
pi@raspberrypi:~ $ pip install https://github.com/lhelontra/tensorflow-on-arm/
    releases/download/v2.4.0/tensorflow-2.4.0-cp37-none-linux_armv7l.whl
pi@raspberrypi:~ $ pip install numpy==1.21.6
pi@raspberrypi:~ $ pip install keras==2.4.0
pi@raspberrypi:~ $ pip install Pillow==9.1.0 
pi@raspberrypi:~ $ pip install protobuf==3.20 
```

#### インストールの確認

```
# TensorFlowの確認
pi@raspberrypi:~ $ python -c 'import tensorflow as tf; print(tf.__version__)'
2.4.0

# Kerasの確認
pi@raspberrypi:~ $ python -c 'import keras; print(keras.__version__)'
Using TensorFlow backend.
2.4.0
```

---

### カメラモジュールの動作確認

#### カメラモジュールが認識されているか確認するコマンド

```
pi@raspberrypi:~ $ vcgencmd get_camera
supported=1 detected=1                    # 両方とも1であれば、認識されている
```

#### 撮影コマンド

```
pi@raspberrypi:~ $ raspistill -o Desktop/image.jpg

pi@raspberrypi:~ $ raspivid -o Desktop/video.h264
```

---

### Google Teachable Machine

<https://teachablemachine.withgoogle.com/train/image>


---

### SunFounder Da Vinci Kit for Raspberry Pi

<https://docs.sunfounder.com/projects/davinci-kit/en/latest/component_list.html>

---

### AI系サービス

#### Quick, Draw!

https://quickdraw.withgoogle.com/

#### AI Programmer

https://aiprogrammer.hashlab.jp/

#### AI校正ツール Shodo

https://shodo.ink/

#### 文章要約AI タンテキ

https://ai-tanteki.com/
