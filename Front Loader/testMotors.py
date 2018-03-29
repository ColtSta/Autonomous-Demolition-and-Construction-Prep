import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

leftWheelF = 16
leftWheelR = 21
rightWheelF = 17
rightWheelR = 27
loaderU = 24
loaderD = 23

GPIO.setup(leftWheelF,GPIO.OUT)
GPIO.setup(leftWheelR,GPIO.OUT)
GPIO.setup(rightWheelF,GPIO.OUT)
GPIO.setup(rightWheelR,GPIO.OUT)
GPIO.setup(loaderU,GPIO.OUT)
GPIO.setup(loaderD,GPIO.OUT)

while True:
	command = raw_input("Direction: ")
	if command == 'w':
		GPIO.output(leftWheelF,GPIO.HIGH)
		GPIO.output(rightWheelF,GPIO.HIGH)
		time.sleep(1)
		GPIO.output(leftWheelF,GPIO.LOW)
		GPIO.output(rightWheelF,GPIO.LOW)
	elif command == 'a':
		GPIO.output(leftWheelR,GPIO.HIGH)
		GPIO.output(rightWheelF,GPIO.HIGH)
		time.sleep(.5)
		GPIO.output(leftWheelR,GPIO.LOW)
		GPIO.output(rightWheelF,GPIO.LOW)
	else:
		break
