import pygame
from pygame.locals import *
from rm_s1_hacker import *
import time
import os

# ssh接続だとディスプレイが開けないので
# DummyVideoDriverを使用する
os.environ["SDL_VIDEODRIVER"] = "dummy"

def joy_demo():
  pygame.init()
  pygame.joystick.init()
  joys = pygame.joystick.Joystick(0)
  joys.init()
  joystick = pygame.joystick.Joystick(0)
  joystick.init()

  hacker = RoboMasterHacker()
  vx = 1024
  vy = 1024
  z = 1024

  try:
    while True:

      for e in pygame.event.get():
        if e.type == pygame.locals.JOYAXISMOTION:
          vx = 1024 - joystick.get_axis(1) * 300
          vy = 1024 + joystick.get_axis(0) * 300
        elif e.type == pygame.locals.JOYBUTTONDOWN:
          print('buttin: ' + str(e.button) + ' pushed')
        elif e.type == pygame.locals.JOYBUTTONUP:
          print('button: ' + str(e.button) + ' released')

      hacker.receive_msg()

      hacker.send_touch_command()
      hacker.send_joy_command(int(vx), int(vy), z)
        
  except KeyboardInterrupt:
    hacker.shutdown()

if __name__ == '__main__':
  joy_demo()