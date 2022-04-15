import can
import time
from . import crc
from . import command_table

class RoboMasterHacker:

  def __init__(self):
    print("----------------------can open----------------------")
    self.bus = can.interface.Bus('can0', bustype='socketcan')
    self.cmd_counter = {}
    self.cmd_counter["joy"] = 0
    self.cmd_counter["led"] = 0
    self.cmd_counter["gimbal"] = 0
    print("generated can bus")

  def shutdown(self):
    print("----------------------shutdown----------------------")
    self.bus.close()
    self.bus.shutdown()

  def receive_msg(self, timeout=0.2):
    received_msg = self.bus.recv(timeout)
    if received_msg is None:
        print('Time out')
    else:
      id = received_msg.arbitration_id
      if id == 0x201:
        recv_data = list(received_msg.data)
        if recv_data[0:6] == [0x55, 0x1b, 0x04, 0x75, 0x09, 0xc3]:
          self.cmd_counter["joy"] = (recv_data[6] | (recv_data[7]<<8) ) + 1
    
  def boot_robomaster(self):
    cmd = self.boot_command()
    cmd += self.led_on_command()
    can_cmd = self.command_reshape(cmd)
    self.send_msg(can_cmd)
  
  def twist_robomaster(self, vx, vy, rz):
    cmd = self.twist_command(vx, vy, rz)
    cmd += self.gimbal_command(0, rz)
    can_cmd = self.command_reshape(cmd)
    self.send_msg(can_cmd)
    
  def control_led(self, r, g, b):
    cmd = self.led_command(r, g, b)
    can_cmd = self.command_reshape(cmd)
    self.send_msg(can_cmd)

  def command_reshape(self, command):
    can_command_list = []
    for i in range(int(len(command)/8+0.99)):
      can_command_list.append(command[0+i*8:8+i*8])
    return can_command_list

  def boot_command(self):
    for command_no in range(26,35):
      header_command = []
      command_length = command_table.command_list[command_no][1]
      for i in range(command_length-2):
        if (i == 3 and command_table.command_list[command_no][3] == 0xFF):
          crc.appendCRC8CheckSum(header_command)
        else:
          header_command.append(command_table.command_list[command_no][i])
      crc.appendCRC16CheckSum(header_command)
      return header_command
  
  def led_on_command(self):
    command_no = 11
    header_command = []
    command_length = command_table.command_list[command_no][1]
    for i in range(command_length-2):
      if (i == 3 and command_table.command_list[command_no][3] == 0xFF):
        crc.appendCRC8CheckSum(header_command)
      elif (i == 6 and command_table.command_list[command_no][6] == 0xFF):
        header_command.append(self.cmd_counter["led"] & 0xFF)
      elif (i == 7 and command_table.command_list[command_no][7] == 0xFF):
        header_command.append( (self.cmd_counter["led"] >> 8) & 0xFF )
      else:
        header_command.append(command_table.command_list[command_no][i])
    crc.appendCRC16CheckSum(header_command)
    self.cmd_counter["led"] += 1
    return header_command

  def led_command(self, red, green, blue):
    for command_no in range(9, 11):
      header_command = []
      command_length = command_table.command_list[command_no][1]
      for i in range(command_length-2):
        if (i == 3 and command_table.command_list[command_no][3] == 0xFF):
          crc.appendCRC8CheckSum(header_command)
        elif (i == 6 and command_table.command_list[command_no][6] == 0xFF):
          header_command.append(self.cmd_counter["led"] & 0xFF)
        elif (i == 7 and command_table.command_list[command_no][7] == 0xFF):
          header_command.append( (self.cmd_counter["led"] >> 8) & 0xFF )
        # RED
        elif i == 14:
          header_command.append(red)
        # GREEN
        elif i == 15:
          header_command.append(green)
        # BLUE
        elif i == 16:
          header_command.append(blue)
        else:
          header_command.append(command_table.command_list[command_no][i])
      crc.appendCRC16CheckSum(header_command)
      self.cmd_counter["led"] += 1
      return header_command

  def send_touch_command(self):
    start_time_touch = time.time()
    touch_msg_list = [[0x55, 0x0f, 0x04, 0xa2, 0x09, 0x04, self.cmd_counter["joy"]&0xFF, (self.cmd_counter["joy"]>>8)&0xFF],
                      [0x40, 0x04, 0x4c, 0x00, 0x00]]
    ucCRC16_2 = crc.getCRC16CheckSum(touch_msg_list[0]+touch_msg_list[1], crc.CRC16_INIT)
    touch_msg_list[1].append( ucCRC16_2 & 0xFF )
    touch_msg_list[1].append( (ucCRC16_2>>8) & 0xFF )
    self.send_msg(touch_msg_list)
    self.cmd_counter["joy"] += 1

  def twist_command(self, vx, vy, vz):
    command_no = 5
    command_length = command_table.command_list[command_no][1]
    header_command = []

    # Linear X and Y
    linear_x = int(256 * vx + 1024)
    linear_y = int(256 * vy + 1024)
    angular_z = int(256 * vz + 1024)

    for i in range(command_length-2):
      if (i == 3 and command_table.command_list[command_no][3] == 0xFF):
        crc.appendCRC8CheckSum(header_command)
      elif (i == 6 and command_table.command_list[command_no][6] == 0xFF):
        header_command.append(self.cmd_counter["joy"] & 0xFF)
      elif (i == 7 and command_table.command_list[command_no][7] == 0xFF):
        header_command.append( (self.cmd_counter["joy"] >> 8) & 0xFF )
      elif i == 13:
        tmp = command_table.command_list[command_no][i] & 0xC0
        tmp |= (linear_x >> 5) & 0x3F
        header_command.append(tmp)
      elif i == 12:
        tmp = (linear_x << 3) & 0xFF;
        tmp |= (linear_y >> 8) & 0x07
        header_command.append(tmp)
      elif i == 11:
        tmp = linear_y & 0xFF
        header_command.append(tmp)
      elif i == 17:
        tmp = (angular_z >> 4) & 0xFF; #0x40
        header_command.append(tmp)
      elif i == 16:
        tmp = ((angular_z << 4)&0xFF) | 0x08; #0x08
        header_command.append(tmp)
      elif i == 18:
        tmp = 0x00
        header_command.append(tmp)
      elif i == 19:
        tmp = 0x02 | ((angular_z << 2) & 0xFF)
        header_command.append(tmp)
      elif i == 20:
        tmp = (angular_z >> 6) & 0xFF # 0x10
        header_command.append(tmp)
      elif i == 21:
        tmp = 0x04
        header_command.append(tmp)
      elif i == 22:
        tmp = 0x0C # Enable Flag 4:x-y 8:yaw 0x0c
        header_command.append(tmp)
      elif i == 23:
        tmp = 0x00
        header_command.append(tmp)
      elif i == 24:
        tmp = 0x04
        header_command.append(tmp)
      else:
        header_command.append(command_table.command_list[command_no][i])
    self.cmd_counter["joy"] += 1
    crc.appendCRC16CheckSum(header_command)
    return header_command

  def gimbal_command(self, ry, rz):
    command_no = 4
    command_length = command_table.command_list[command_no][1]
    header_command = []

    # Angular X and Y
    angular_y = int(-1024 * ry)
    angular_z = int(-1024 * rz)

    for i in range(command_length-2):
      if (i == 3 and command_table.command_list[command_no][3] == 0xFF):
        crc.appendCRC8CheckSum(header_command)
      elif (i == 6 and command_table.command_list[command_no][6] == 0xFF):
        header_command.append(self.cmd_counter["gimbal"] & 0xFF)
      elif (i == 7 and command_table.command_list[command_no][7] == 0xFF):
        header_command.append( (self.cmd_counter["gimbal"] >> 8) & 0xFF )
      elif i == 14:
        header_command.append( (angular_y >> 8) & 0xFF )
      elif i == 13:
        header_command.append( angular_y & 0xFF )
      elif i == 16:
        header_command.append( (angular_z >> 8) & 0xFF )
      elif i == 15:
        header_command.append( angular_z & 0xFF )
      else:
        header_command.append(command_table.command_list[command_no][i])
    self.cmd_counter["gimbal"] += 1
    crc.appendCRC16CheckSum(header_command)
    return header_command

  def send_msg(self, msg_list):
    for msg in msg_list:
      send_msg = can.Message(arbitration_id=0x201, data=msg, is_extended_id=False)
      self.bus.send(send_msg)

if __name__ == '__main__':
  print("Hello")