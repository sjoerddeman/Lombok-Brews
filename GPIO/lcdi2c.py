#!/usr/bin/python

import smbus
import sys
import time
import datetime

I2C_ADDR  = 0x27 # I2C device address
LCD_WIDTH = 16   # Maximum characters per line

# Define some device constants
LCD_CHR = 1 # Mode - Sending data
LCD_CMD = 0 # Mode - Sending command

LCD_LINE_1 = 0x80 # LCD RAM address for the 1st line
LCD_LINE_2 = 0xC0 # LCD RAM address for the 2nd line

LCD_BACKLIGHT  = 0x08  # On 0X08 / Off 0x00

ENABLE = 0b00000100 # Enable bit

E_PULSE = 0.0005
E_DELAY = 0.0005

bus = smbus.SMBus(1) # Rev 2 Pi uses 1

def lcd_init():
  lcd_byte(0x33,LCD_CMD) # 110011 Initialise
  lcd_byte(0x32,LCD_CMD) # 110010 Initialise
  lcd_byte(0x06,LCD_CMD) # 000110 Cursor move direction
  lcd_byte(0x0C,LCD_CMD) # 001100 Display On,Cursor Off, Blink Off
  lcd_byte(0x28,LCD_CMD) # 101000 Data length, number of lines, font size
  lcd_byte(0x01,LCD_CMD) # 000001 Clear display
  time.sleep(E_DELAY)

def lcd_byte(bits, mode):

  bits_high = mode | (bits & 0xF0) | LCD_BACKLIGHT
  bits_low = mode | ((bits<<4) & 0xF0) | LCD_BACKLIGHT

  bus.write_byte(I2C_ADDR, bits_high)
  lcd_toggle_enable(bits_high)

  bus.write_byte(I2C_ADDR, bits_low)
  lcd_toggle_enable(bits_low)

def lcd_toggle_enable(bits):
  time.sleep(E_DELAY)
  bus.write_byte(I2C_ADDR, (bits | ENABLE))
  time.sleep(E_PULSE)
  bus.write_byte(I2C_ADDR,(bits & ~ENABLE))
  time.sleep(E_DELAY)

def lcd_string(message,line):

  message = message.ljust(LCD_WIDTH," ")

  lcd_byte(line, LCD_CMD)

  for i in range(LCD_WIDTH):
    lcd_byte(ord(message[i]),LCD_CHR)

def temp_message(temp, min, max):

  lcd_init()
  action = "Temp OK"
  if(temp < min):
    action = "Heating"
  if(temp > max):
    action = "Cooling"

  lcd_string(str(min) + chr(223) + "C - " + str(max) + chr(223) + "C",LCD_LINE_1)
  lcd_string(str(temp) + chr(223) + "C: " + action, LCD_LINE_2)
  time.sleep(1)

def main(message1, message2):

  lcd_init()

  while True:

    lcd_string(message1,LCD_LINE_1)
    lcd_string(message2,LCD_LINE_2)
    time.sleep(10)

if __name__ == '__main__':

  try:
    # count the arguments
    arguments = len(sys.argv) - 1

    # output argument-wise
    position = 1
    message1 = ""
    message2 = ""
    while (arguments >= position):
        if(position == 1):
          message1 = sys.argv[position]
        if(position == 2):
          message2 = sys.argv[position]          
        position = position + 1
    main(message1, message2)
  except KeyboardInterrupt:
    pass
  finally:
    lcd_byte(0x01, LCD_CMD)



