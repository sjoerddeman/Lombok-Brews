#!/usr/bin/env python3

# Raspberry Pi Python 3 TM1637 quad 7-segment LED display driver examples

import tm1637
import time

CLK=27
DIO=17

tm = tm1637.TM1637(clk=CLK, dio=DIO)

def set_temp(temp, msg):
	#tm.scroll(msg) # 4 fps
	temp_str = str(int(temp*10))
	tm.write([tm.encode_char(temp_str[0]), tm.encode_char(temp_str[1]), tm.encode_char(temp_str[2]), 99])

def turn_off():
	tm.write([0, 0, 0, 0])

def set_display(temp, min, max):
	if(temp > max):
		print(str(temp) + ": koelkast aan")
		set_temp(temp, (str(int(min*10))+"-"+str(int(max*10))+" BIER AFKOELEN"))
	elif(temp < min):
		print(str(temp) + ": verwarming aan")
		set_temp(temp, (str(int(min*10))+"-"+str(int(max*10))+" BIER VERHITTEN"))
	else:
		print(str(temp) + ": temperatuur oké")
		set_temp(temp, (str(int(min*10))+"-"+str(int(max*10))+" BIER OKE"))
