from rm_s1_hacker import *
import time
import os
import paho.mqtt.client as mqtt

def on_connect(client, userdata, flag, rc):
  print("Connected with result code " + str(rc))
  client.subscribe("Joy/x") 
  client.subscribe("Joy/y") 

def on_disconnect(client, userdata, flag, rc):
  if  rc != 0:
    print("Unexpected disconnection.")

joy_x = 0
joy_y = 0

def on_message(client, userdata, msg):
  global joy_x
  global joy_y
  if msg.topic == "Joy/x":
    joy_x = int(msg.payload)
  elif msg.topic == "Joy/y":
    joy_y = int(msg.payload)

def joy_demo():

  client = mqtt.Client()
  client.on_connect = on_connect
  client.on_disconnect = on_disconnect
  client.on_message = on_message
  client.connect("localhost", 1884, 60)
  #client.loop_forever()
  client.loop_start()

  hacker = RoboMasterHacker()
  start_time = time.time()
  start_time_touch = time.time()
  send_interval = 0.001
  send_interval_touch = 0.001
  vx = 1024
  vy = 1024
  z = 1024

  try:
    while True:

      vx = 1024 - joy_y
      vy = 1024 + joy_x

      hacker.receive_msg()
      hacker.send_touch_command()
      hacker.send_joy_command(int(vx), int(vy), z)
        
  except KeyboardInterrupt:
    hacker.shutdown()

if __name__ == '__main__':
  joy_demo()