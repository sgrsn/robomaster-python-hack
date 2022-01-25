import can
import time

CRC8_INIT = 119
CRC8_TABLE = [
  0x00, 0x5e, 0xbc, 0xe2, 0x61, 0x3f, 0xdd, 0x83, 0xc2, 0x9c, 0x7e, 0x20, 0xa3, 0xfd, 0x1f, 0x41,
  0x9d, 0xc3, 0x21, 0x7f, 0xfc, 0xa2, 0x40, 0x1e, 0x5f, 0x01, 0xe3, 0xbd, 0x3e, 0x60, 0x82, 0xdc,
  0x23, 0x7d, 0x9f, 0xc1, 0x42, 0x1c, 0xfe, 0xa0, 0xe1, 0xbf, 0x5d, 0x03, 0x80, 0xde, 0x3c, 0x62,
  0xbe, 0xe0, 0x02, 0x5c, 0xdf, 0x81, 0x63, 0x3d, 0x7c, 0x22, 0xc0, 0x9e, 0x1d, 0x43, 0xa1, 0xff,
  0x46, 0x18, 0xfa, 0xa4, 0x27, 0x79, 0x9b, 0xc5, 0x84, 0xda, 0x38, 0x66, 0xe5, 0xbb, 0x59, 0x07,
  0xdb, 0x85, 0x67, 0x39, 0xba, 0xe4, 0x06, 0x58, 0x19, 0x47, 0xa5, 0xfb, 0x78, 0x26, 0xc4, 0x9a,
  0x65, 0x3b, 0xd9, 0x87, 0x04, 0x5a, 0xb8, 0xe6, 0xa7, 0xf9, 0x1b, 0x45, 0xc6, 0x98, 0x7a, 0x24,
  0xf8, 0xa6, 0x44, 0x1a, 0x99, 0xc7, 0x25, 0x7b, 0x3a, 0x64, 0x86, 0xd8, 0x5b, 0x05, 0xe7, 0xb9,
  0x8c, 0xd2, 0x30, 0x6e, 0xed, 0xb3, 0x51, 0x0f, 0x4e, 0x10, 0xf2, 0xac, 0x2f, 0x71, 0x93, 0xcd,
  0x11, 0x4f, 0xad, 0xf3, 0x70, 0x2e, 0xcc, 0x92, 0xd3, 0x8d, 0x6f, 0x31, 0xb2, 0xec, 0x0e, 0x50,
  0xaf, 0xf1, 0x13, 0x4d, 0xce, 0x90, 0x72, 0x2c, 0x6d, 0x33, 0xd1, 0x8f, 0x0c, 0x52, 0xb0, 0xee,
  0x32, 0x6c, 0x8e, 0xd0, 0x53, 0x0d, 0xef, 0xb1, 0xf0, 0xae, 0x4c, 0x12, 0x91, 0xcf, 0x2d, 0x73,
  0xca, 0x94, 0x76, 0x28, 0xab, 0xf5, 0x17, 0x49, 0x08, 0x56, 0xb4, 0xea, 0x69, 0x37, 0xd5, 0x8b,
  0x57, 0x09, 0xeb, 0xb5, 0x36, 0x68, 0x8a, 0xd4, 0x95, 0xcb, 0x29, 0x77, 0xf4, 0xaa, 0x48, 0x16,
  0xe9, 0xb7, 0x55, 0x0b, 0x88, 0xd6, 0x34, 0x6a, 0x2b, 0x75, 0x97, 0xc9, 0x4a, 0x14, 0xf6, 0xa8,
  0x74, 0x2a, 0xc8, 0x96, 0x15, 0x4b, 0xa9, 0xf7, 0xb6, 0xe8, 0x0a, 0x54, 0xd7, 0x89, 0x6b, 0x35]

CRC16_INIT = 13970
CRC16_TABLE = [
  0x0000, 0x1189, 0x2312, 0x329b, 0x4624, 0x57ad, 0x6536, 0x74bf,
  0x8c48, 0x9dc1, 0xaf5a, 0xbed3, 0xca6c, 0xdbe5, 0xe97e, 0xf8f7,
  0x1081, 0x0108, 0x3393, 0x221a, 0x56a5, 0x472c, 0x75b7, 0x643e,
  0x9cc9, 0x8d40, 0xbfdb, 0xae52, 0xdaed, 0xcb64, 0xf9ff, 0xe876,
  0x2102, 0x308b, 0x0210, 0x1399, 0x6726, 0x76af, 0x4434, 0x55bd,
  0xad4a, 0xbcc3, 0x8e58, 0x9fd1, 0xeb6e, 0xfae7, 0xc87c, 0xd9f5,
  0x3183, 0x200a, 0x1291, 0x0318, 0x77a7, 0x662e, 0x54b5, 0x453c,
  0xbdcb, 0xac42, 0x9ed9, 0x8f50, 0xfbef, 0xea66, 0xd8fd, 0xc974,
  0x4204, 0x538d, 0x6116, 0x709f, 0x0420, 0x15a9, 0x2732, 0x36bb,
  0xce4c, 0xdfc5, 0xed5e, 0xfcd7, 0x8868, 0x99e1, 0xab7a, 0xbaf3,
  0x5285, 0x430c, 0x7197, 0x601e, 0x14a1, 0x0528, 0x37b3, 0x263a,
  0xdecd, 0xcf44, 0xfddf, 0xec56, 0x98e9, 0x8960, 0xbbfb, 0xaa72,
  0x6306, 0x728f, 0x4014, 0x519d, 0x2522, 0x34ab, 0x0630, 0x17b9,
  0xef4e, 0xfec7, 0xcc5c, 0xddd5, 0xa96a, 0xb8e3, 0x8a78, 0x9bf1,
  0x7387, 0x620e, 0x5095, 0x411c, 0x35a3, 0x242a, 0x16b1, 0x0738,
  0xffcf, 0xee46, 0xdcdd, 0xcd54, 0xb9eb, 0xa862, 0x9af9, 0x8b70,
  0x8408, 0x9581, 0xa71a, 0xb693, 0xc22c, 0xd3a5, 0xe13e, 0xf0b7,
  0x0840, 0x19c9, 0x2b52, 0x3adb, 0x4e64, 0x5fed, 0x6d76, 0x7cff,
  0x9489, 0x8500, 0xb79b, 0xa612, 0xd2ad, 0xc324, 0xf1bf, 0xe036,
  0x18c1, 0x0948, 0x3bd3, 0x2a5a, 0x5ee5, 0x4f6c, 0x7df7, 0x6c7e,
  0xa50a, 0xb483, 0x8618, 0x9791, 0xe32e, 0xf2a7, 0xc03c, 0xd1b5,
  0x2942, 0x38cb, 0x0a50, 0x1bd9, 0x6f66, 0x7eef, 0x4c74, 0x5dfd,
  0xb58b, 0xa402, 0x9699, 0x8710, 0xf3af, 0xe226, 0xd0bd, 0xc134,
  0x39c3, 0x284a, 0x1ad1, 0x0b58, 0x7fe7, 0x6e6e, 0x5cf5, 0x4d7c,
  0xc60c, 0xd785, 0xe51e, 0xf497, 0x8028, 0x91a1, 0xa33a, 0xb2b3,
  0x4a44, 0x5bcd, 0x6956, 0x78df, 0x0c60, 0x1de9, 0x2f72, 0x3efb,
  0xd68d, 0xc704, 0xf59f, 0xe416, 0x90a9, 0x8120, 0xb3bb, 0xa232,
  0x5ac5, 0x4b4c, 0x79d7, 0x685e, 0x1ce1, 0x0d68, 0x3ff3, 0x2e7a,
  0xe70e, 0xf687, 0xc41c, 0xd595, 0xa12a, 0xb0a3, 0x8238, 0x93b1,
  0x6b46, 0x7acf, 0x4854, 0x59dd, 0x2d62, 0x3ceb, 0x0e70, 0x1ff9,
  0xf78f, 0xe606, 0xd49d, 0xc514, 0xb1ab, 0xa022, 0x92b9, 0x8330,
  0x7bc7, 0x6a4e, 0x58d5, 0x495c, 0x3de3, 0x2c6a, 0x1ef1, 0x0f78]


command_list = [[0,10,0x55,0x0D,0x04,0xFF,0x0A,0xFF,0xFF,0xFF,0x40,0x00,0x01,0xFF,0xFF,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                [1,10,0x55,0x0E,0x04,0xFF,0x09,0x03,0xFF,0xFF,0xA0,0x48,0x08,0x01,0xFF,0xFF,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                [2,10,0x55,0x0F,0x04,0xFF,0xF1,0xC3,0xFF,0xFF,0x00,0x0A,0x53,0x32,0x00,0xFF,0xFF,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                [3,100,0x55,0x12,0x04,0xFF,0xF1,0xC3,0xFF,0xFF,0x40,0x00,0x58,0x03,0x92,0x06,0x02,0x00,0xFF,0xFF,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                [4,1,0x55,0x14,0x04,0xFF,0x09,0x04,0xFF,0xFF,0x00,0x04,0x69,0x08,0x05,0x00,0x00,0x00,0x00,0x6D,0xFF,0xFF,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                [5,1,0x55,0x1B,0x04,0xFF,0x09,0xC3,0xFF,0xFF,0x00,0x3F,0x60,0x00,0x04,0x20,0x00,0x01,0x08,0x40,0x00,0x02,0x10,0x04,0x03,0x00,0x04,0xA3,0x88,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                [6,100,0x55,0x49,0x04,0xFF,0x49,0x03,0xFF,0xFF,0x00,0x3F,0x70,0xB4,0x11,0x34,0x03,0x00,0x00,0xF7,0x05,0x42,0x08,0x10,0x00,0x08,0x00,0x08,0x00,0x08,0x00,0x08,0x00,0x08,0x00,0x08,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x7E,0x0E,0xF3,0x0B,0xD9,0x07,0x0E,0x07,0x3D,0x07,0x6A,0x08,0x62,0x0A,0x05,0x0B,0xD6,0x0B,0xFF,0xFF],
                [7,0xFF,0x55,0x0E,0x04,0xFF,0x09,0x17,0xFF,0xFF,0x00,0x3F,0x51,0x11,0xFF,0xFF,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                [8,0xFF,0x55,0x16,0x04,0xFF,0x09,0x17,0xFF,0xFF,0x00,0x3F,0x55,0x73,0x00,0xFF,0x00,0x01,0x28,0x00,0x00,0x00,0xFF,0xFF,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                [9,0xFF,0x55,0x1A,0x04,0xFF,0x09,0x18,0xFF,0xFF,0x00,0x3F,0x32,0x05,0xFF,0x00,0x00,0x7F,0x46,0x00,0x64,0x00,0x64,0x00,0x30,0x00,0xFF,0xFF,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                [10,0xFF,0x55,0x1A,0x04,0xFF,0x09,0x18,0xFF,0xFF,0x00,0x3F,0x32,0x01,0xFF,0x00,0x00,0x7F,0x46,0x00,0xC8,0x00,0xC8,0x00,0x0F,0x00,0xFF,0xFF,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                [11,0xFF,0x55,0x1A,0x04,0xFF,0x09,0x18,0xFF,0xFF,0x00,0x3F,0x32,0x01,0xFF,0x00,0x00,0x7F,0x46,0x00,0x00,0x00,0x00,0x00,0x3F,0x00,0xFF,0xFF,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                [12,0xFF,0x55,0x1A,0x04,0xFF,0x09,0x18,0xFF,0xFF,0x00,0x3F,0x32,0x02,0xFF,0x00,0xFF,0xFF,0xFF,0x00,0xF4,0x01,0xF4,0x01,0x3F,0x00,0xFF,0xFF,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                [13,0xFF,0x55,0x1A,0x04,0xFF,0x09,0x18,0xFF,0xFF,0x00,0x3F,0x32,0x73,0xFF,0x00,0xFF,0x00,0x00,0x01,0x64,0x00,0x0A,0x00,0x3F,0x00,0xFF,0xFF,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                [14,0xFF,0x55,0x1A,0x04,0xFF,0x09,0x18,0xFF,0xFF,0x00,0x3F,0x32,0x05,0xF0,0x00,0xC8,0x00,0x00,0x00,0x64,0x00,0x64,0x00,0x30,0x00,0xFF,0xFF,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                [15,0xFF,0x55,0x1A,0x04,0xFF,0x09,0x18,0xFF,0xFF,0x00,0x3F,0x32,0x01,0xFF,0x00,0xC8,0x00,0x00,0x00,0xC8,0x00,0xC8,0x00,0x0F,0x00,0xFF,0xFF,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                [16,0xFF,0x55,0x1A,0x04,0xFF,0x09,0x18,0xFF,0xFF,0x00,0x3F,0x32,0x05,0xF0,0x00,0x00,0x00,0xFF,0x00,0x64,0x00,0x64,0x00,0x30,0x00,0xFF,0xFF,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                [17,0xFF,0x55,0x1A,0x04,0xFF,0x09,0x18,0xFF,0xFF,0x00,0x3F,0x32,0x01,0xFF,0x00,0x00,0x00,0xFF,0x00,0xC8,0x00,0xC8,0x00,0x0F,0x00,0xFF,0xFF,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                [18,0xFF,0x55,0x1A,0x04,0xFF,0x09,0x18,0xFF,0xFF,0x00,0x3F,0x32,0x05,0xF0,0x00,0x00,0xFF,0x00,0x00,0x64,0x00,0x64,0x00,0x30,0x00,0xFF,0xFF,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                [19,0xFF,0x55,0x1A,0x04,0xFF,0x09,0x18,0xFF,0xFF,0x00,0x3F,0x32,0x01,0xFF,0x00,0x00,0xFF,0x00,0x00,0xC8,0x00,0xC8,0x00,0x0F,0x00,0xFF,0xFF,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                [20,100,0x55,0x0F,0x04,0xFF,0x09,0x04,0xFF,0xFF,0x40,0x04,0x4C,0x00,0x00,0xFF,0xFF,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                [21,0xFF,0x55,0x0F,0x04,0xFF,0x09,0x04,0xFF,0xFF,0x40,0x04,0x4C,0x02,0x00,0xFF,0xFF,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                [22,0xFF,0x55,0x0E,0x04,0xFF,0x09,0xC3,0xFF,0xFF,0x40,0x3F,0x3F,0x01,0xFF,0xFF,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                [23,0xFF,0x55,0x0E,0x04,0xFF,0x09,0xC3,0xFF,0xFF,0x40,0x3F,0x3F,0x02,0xFF,0xFF,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                [24,0xFF,0x55,0x0E,0x04,0xFF,0x09,0xC3,0xFF,0xFF,0x40,0x3F,0x3F,0x03,0xFF,0xFF,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                [25,0xFF,0x55,0x0E,0x04,0xFF,0x09,0xC3,0xFF,0xFF,0x40,0x3F,0x3F,0x04,0xFF,0xFF,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                [26,0xFF,0x55,0x1B,0x04,0xFF,0x09,0xC3,0x00,0x00,0x00,0x3F,0x60,0x00,0x04,0x20,0x00,0x01,0x00,0x40,0x00,0x02,0x10,0x00,0x03,0x00,0x00,0xFF,0xFF,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                [27,0xFF,0x55,0x14,0x04,0xFF,0x09,0x04,0x00,0x00,0x00,0x04,0x69,0x08,0x05,0x00,0x00,0x00,0x00,0x01,0xFF,0xFF,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                [28,0xFF,0x55,0x0F,0x04,0xFF,0x09,0x04,0x02,0x00,0x40,0x04,0x4C,0x02,0x00,0xFF,0xFF,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                [29,0xFF,0x55,0x0E,0x04,0xFF,0x09,0x03,0x00,0x00,0x00,0x3F,0x3F,0x02,0xFF,0xFF,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                [30,0xFF,0x55,0x15,0x04,0xFF,0xF1,0xC3,0x00,0x00,0x00,0x03,0xD7,0x01,0x07,0x00,0x02,0x00,0x00,0x00,0x00,0xFF,0xFF,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                [31,0xFF,0x55,0x12,0x04,0xFF,0x09,0x03,0x01,0x00,0x40,0x48,0x01,0x09,0x00,0x00,0x00,0x03,0xFF,0xFF,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                [32,0xFF,0x55,0x1C,0x04,0xFF,0x09,0x03,0x02,0x00,0x40,0x48,0x03,0x09,0x00,0x03,0x00,0x01,0xFB,0xDC,0xF5,0xD7,0x03,0x00,0x02,0x00,0x01,0x00,0xFF,0xFF,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                [33,0xFF,0x55,0x12,0x04,0xFF,0x09,0x03,0x03,0x00,0x40,0x48,0x01,0x09,0x00,0x00,0x00,0x03,0xFF,0xFF,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                [34,0xFF,0x55,0x24,0x04,0xFF,0x09,0x03,0x04,0x00,0x40,0x48,0x03,0x09,0x01,0x03,0x00,0x02,0xA7,0x02,0x29,0x88,0x03,0x00,0x02,0x00,0x66,0x3E,0x3E,0x4C,0x03,0x00,0x02,0x00,0x32,0x00,0xFF,0xFF,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                [35,0xFF,0x55,0x3C,0x04,0xFF,0x09,0x03,0x05,0x00,0x40,0x48,0x03,0x09,0x02,0x03,0x00,0x05,0x09,0xA3,0x26,0xE2,0x03,0x00,0x02,0x00,0xB3,0xF7,0xE6,0x47,0x03,0x00,0x02,0x00,0xF4,0x1D,0x1C,0xDC,0x03,0x00,0x02,0x00,0x03,0xC5,0x58,0x08,0x03,0x00,0x02,0x00,0x42,0xEE,0x13,0x1D,0x03,0x00,0x02,0x00,0x05,0x00,0xFF,0xFF,0,0,0,0,0,0,0,0,0,0,0,0,0],
                [36,0xFF,0x55,0x0F,0x04,0xFF,0x09,0x04,0xFF,0xFF,0x00,0x04,0x0D,0xB5,0x2A,0xFF,0xFF,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                [37,0xFF,0x55,0x0F,0x04,0xFF,0x09,0x04,0xFF,0xFF,0x00,0x04,0x0D,0xF2,0x7E,0xFF,0xFF,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]]


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
      idx = 0
      command_length = command_list[command_no][3]
      for i in range(2, command_length):
        if (i == 5 and command_list[command_no][5] == 0xFF):
          self.appendCRC8CheckSum(header_command)
        else:
          header_command.append(command_list[command_no][i])
      self.appendCRC16CheckSum(header_command)
      return header_command
  
  def led_on_command(self):
    command_no = 11
    header_command = []
    idx = 0
    command_length = command_list[command_no][3]
    for i in range(2, command_length):
      if (i == 5 and command_list[command_no][5] == 0xFF):
        self.appendCRC8CheckSum(header_command)
      elif (i == 8 and command_list[command_no][8] == 0xFF):
        header_command.append(self.cmd_counter["led"] & 0xFF)
      elif (i == 9 and command_list[command_no][9] == 0xFF):
        header_command.append( (self.cmd_counter["led"] >> 8) & 0xFF )
      else:
        header_command.append(command_list[command_no][i])
    self.appendCRC16CheckSum(header_command)
    self.cmd_counter["led"] += 1
    return header_command

  def led_command(self, red, green, blue):
    for command_no in range(9, 11):
      header_command = []
      command_length = command_list[command_no][3]
      for i in range(2,command_length):
        if (i == 5 and command_list[command_no][5] == 0xFF):
          self.appendCRC8CheckSum(header_command)
        elif (i == 8 and command_list[command_no][8] == 0xFF):
          header_command.append(self.cmd_counter["led"] & 0xFF)
        elif (i == 9 and command_list[command_no][9] == 0xFF):
          header_command.append( (self.cmd_counter["led"] >> 8) & 0xFF )
        # RED
        elif i == 16:
          header_command.append(red)
        # GREEN
        elif i == 17:
          header_command.append(green)
        # BLUE
        elif i == 18:
          header_command.append(blue)
        else:
          header_command.append(command_list[command_no][i])
      self.appendCRC16CheckSum(header_command)
      self.cmd_counter["led"] += 1
      return header_command

  def send_touch_command(self):
    start_time_touch = time.time()
    touch_msg_list = [[0x55, 0x0f, 0x04, 0xa2, 0x09, 0x04, self.cmd_counter["joy"]&0xFF, (self.cmd_counter["joy"]>>8)&0xFF],
                      [0x40, 0x04, 0x4c, 0x00, 0x00]]
    ucCRC16_2 = self.getCRC16CheckSum(touch_msg_list[0]+touch_msg_list[1], CRC16_INIT)
    touch_msg_list[1].append( ucCRC16_2 & 0xFF )
    touch_msg_list[1].append( (ucCRC16_2>>8) & 0xFF )
    self.send_msg(touch_msg_list)
    self.cmd_counter["joy"] += 1

  def twist_command(self, vx, vy, vz):
    command_no = 5;
    command_length = command_list[command_no][3]
    header_command = []

    # Linear X and Y
    linear_x = int(256 * vx + 1024)
    linear_y = int(256 * vy + 1024)
    angular_z = int(256 * vz + 1024)

    for i in range(2, command_length):
      if (i == 5 and command_list[command_no][5] == 0xFF):
        self.appendCRC8CheckSum(header_command)
      elif (i == 8 and command_list[command_no][8] == 0xFF):
        header_command.append(self.cmd_counter["joy"] & 0xFF)
      elif (i == 9 and command_list[command_no][9] == 0xFF):
        header_command.append( (self.cmd_counter["joy"] >> 8) & 0xFF )
      elif i == 15:
        tmp = command_list[command_no][i] & 0xC0
        tmp |= (linear_x >> 5) & 0x3F
        header_command.append(tmp)
      elif i == 14:
        tmp = (linear_x << 3) & 0xFF;
        tmp |= (linear_y >> 8) & 0x07
        header_command.append(tmp)
      elif i == 13:
        tmp = linear_y & 0xFF
        header_command.append(tmp)
      elif i == 19:
        tmp = (angular_z >> 4) & 0xFF; #0x40
        header_command.append(tmp)
      elif i == 18:
        tmp = ((angular_z << 4)&0xFF) | 0x08; #0x08
        header_command.append(tmp)
      elif i == 20:
        tmp = 0x00
        header_command.append(tmp)
      elif i == 21:
        tmp = 0x02 | ((angular_z << 2) & 0xFF)
        header_command.append(tmp)
      elif i == 22:
        tmp = (angular_z >> 6) & 0xFF # 0x10
        header_command.append(tmp)
      elif i == 23:
        tmp = 0x04
        header_command.append(tmp)
      elif i == 24:
        tmp = 0x0C # Enable Flag 4:x-y 8:yaw 0x0c
        header_command.append(tmp)
      elif i == 25:
        tmp = 0x00
        header_command.append(tmp)
      elif i == 26:
        tmp = 0x04
        header_command.append(tmp)
      else:
        header_command.append(command_list[command_no][i])
    self.cmd_counter["joy"] += 1
    self.appendCRC16CheckSum(header_command)
    return header_command

  def gimbal_command(self, ry, rz):
    command_no = 4
    command_length = command_list[command_no][3]
    header_command = []

    # Angular X and Y
    angular_y = int(-1024 * ry)
    angular_z = int(-1024 * rz)

    for i in range(2,command_length):
      if (i == 5 and command_list[command_no][5] == 0xFF):
        self.appendCRC8CheckSum(header_command)
      elif (i == 8 and command_list[command_no][8] == 0xFF):
        header_command.append(self.cmd_counter["gimbal"] & 0xFF)
      elif (i == 9 and command_list[command_no][9] == 0xFF):
        header_command.append( (self.cmd_counter["gimbal"] >> 8) & 0xFF )
      elif i == 16:
        header_command.append( (angular_y >> 8) & 0xFF )
      elif i == 15:
        header_command.append( angular_y & 0xFF )
      elif i == 18:
        header_command.append( (angular_z >> 8) & 0xFF )
      elif i == 17:
        header_command.append( angular_z & 0xFF )
      else:
        header_command.append(command_list[command_no][i])
    self.cmd_counter["gimbal"] += 1
    self.appendCRC16CheckSum(header_command)
    return header_command

  def send_msg(self, msg_list):
    for msg in msg_list:
      send_msg = can.Message(arbitration_id=0x201, data=msg, is_extended_id=False)
      self.bus.send(send_msg)

  def getCRC8CheckSum(self, pchMessage, ucCRC8):
    ucIndex = 0
    for i in pchMessage:
      ucIndex = ucCRC8 ^ i
      ucCRC8 = CRC8_TABLE[ucIndex]
    return ucCRC8

  def getCRC16CheckSum(self, pchMessage, ucCRC16):
    ucIndex = 0
    for i in pchMessage:
      ucIndex = (ucCRC16 ^ i) & 0xFF
      ucCRC16 = (ucCRC16>>8) ^ CRC16_TABLE[ucIndex]
    return ucCRC16

  def appendCRC8CheckSum(self, pchMessage):
    ucCRC = 0
    ucCRC = self.getCRC8CheckSum(pchMessage, CRC8_INIT)
    pchMessage.append(ucCRC)

  def appendCRC16CheckSum(self, pchMessage):
    ucCRC = 0
    ucCRC = self.getCRC16CheckSum(pchMessage, CRC16_INIT)
    pchMessage.append(ucCRC & 0xFF)
    pchMessage.append((ucCRC>>8) & 0xFF)

if __name__ == '__main__':
  print("Hello")