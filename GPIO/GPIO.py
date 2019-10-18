import sys
sys.path.append('../BrewDB')
import DB
import time
import random
import four_digit
import ds18b20
import threading
from datetime import datetime
from sense_hat import SenseHat

def read_temp():
	temp = ds18b20.read_temp()
	return temp
		
def set_device(temp):
	four_digit.set_display(temp, min, max)

def get_current_program(items):
	current_item = []
	for item in items:
		if(datetime.strptime(item[2], "%Y-%m-%dT%H:%M") <= datetime.now()):
			current_item = item
	return current_item
			

min = 0.0
max = 100.0
started = False
last_temp = 0.0;


while(True):
	items = DB.get_program()
	item = get_current_program(items)
	if(item != []):
		print(str(item[0]) +" - "+ str(item[1]))
		min = float(item[0])
		max = float(item[1]) 
		started = bool(item[2])	
		current_temp = read_temp()
		threading.Thread(target=set_device, args=(current_temp,)).start()
		DB.add_data(current_temp, min, max)	
	else:
		min = 0.0
		max = 100.0
		print("geen actief programma")
	time.sleep(60)

