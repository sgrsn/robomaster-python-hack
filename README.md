# RoboMaster S1 をCANでハックするpythonのコードです

## 要るもの

- Robomaster s1
- Jetson nano
- CANable Pro https://canable.io/
- ジャンパー線3本

## 接続

Jetson nanoにCANableをUSBケーブルで接続
RobomasterのGND, CANH, CANLをCANableと接続、機体後ろ側のLEDがやりやすい

## 動かし方

とりあえず動かす
$ python3 rm_s1_hacker.py

JetsonにJoystickを接続して動かす
$ python3 joy_control.py

mqttを使用して遠隔で動かす

Jetson側
$ mosquitto -p 1884
$ python3 mqtt_control.py

操作側(windowsで確認)
$ python mqtt_joy_pub.py