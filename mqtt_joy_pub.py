#!usr/bin/env python
# -*- coding: utf-8 -*- 
import paho.mqtt.client as mqtt
import pygame
from pygame.locals import *
import os
import time

# ssh接続だとディスプレイが開けないので
# DummyVideoDriverを使用する
os.environ["SDL_VIDEODRIVER"] = "dummy"

def on_connect(client, userdata, flag, rc):
  print("Connected with result code " + str(rc))

def on_disconnect(client, userdata, flag, rc):
  if rc != 0:
     print("Unexpected disconnection.")

def on_publish(client, userdata, mid):
  print("publish: {0}".format(mid))

def joy_demo():
  client = mqtt.Client()
  client.on_connect = on_connect
  client.on_disconnect = on_disconnect
  client.on_publish = on_publish
  client.connect('192.168.0.86', 1884, 60)
  client.loop_start()

  pygame.init()
  pygame.joystick.init()
  joys = pygame.joystick.Joystick(0)
  joys.init()
  joystick = pygame.joystick.Joystick(0)
  joystick.init()

  x = 0
  y = 0

  while True:
    for e in pygame.event.get():
      if e.type == pygame.locals.JOYAXISMOTION:
        x = int(joystick.get_axis(0)*300)
        y = int(joystick.get_axis(1)*300)
      elif e.type == pygame.locals.JOYBUTTONDOWN:
        print('buttin: ' + str(e.button) + ' pushed')
      elif e.type == pygame.locals.JOYBUTTONUP:
        print('button: ' + str(e.button) + ' released')
    
    client.publish("Joy/x", x)
    client.publish("Joy/y", y)

    time.sleep(0.1)

if __name__ == '__main__':
  try:
    joy_demo()
  except KeyboardInterrupt:
    print("終了")