import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

RELAIS_1 = 5
RELAIS_2 = 6

GPIO.setup([RELAIS_1, RELAIS_2], GPIO.OUT)

GPIO.output(RELAIS_1, GPIO.LOW)
GPIO.output(RELAIS_2, GPIO.LOW)

def set_relais_device(temp, min, max):
	if(temp < min):
		GPIO.output(RELAIS_1, GPIO.HIGH)
		GPIO.output(RELAIS_2, GPIO.LOW)
	elif(temp > max):
		GPIO.output(RELAIS_1, GPIO.LOW)
		GPIO.output(RELAIS_2, GPIO.HIGH)
	else:
		GPIO.output(RELAIS_1, GPIO.LOW)
		GPIO.output(RELAIS_2, GPIO.LOW)
