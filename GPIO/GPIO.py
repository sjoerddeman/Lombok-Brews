import sys
sys.path.append('../BrewDB')
import DB
import time
import random
import four_digit
import ds18b20
import lcdi2c
import relais
import threading
from datetime import datetime

def read_temp():
	temp = ds18b20.read_temp()
	return round(temp, 1)
		
def set_device(temp, min, max):
	lcdi2c.temp_message(temp, min, max)
	four_digit.set_display(temp, min, max)
	relais.set_relais_device(temp, min, max)			

while(True):
	items = DB.get_program()
	item = DB.get_current_program_item(items)
	if(item != []):
		print(str(item[0]) +" - "+ str(item[1]))
		min = float(item[0])
		max = float(item[1]) 
		current_temp = read_temp()
		threading.Thread(target=set_device, args=(current_temp, min, max)).start()
		DB.add_data(current_temp, min, max)	
	else:
		print("geen actief programma!")
		DB.add_data(float("NaN"), float("NaN"), float("NaN"))	
	time.sleep(60)

