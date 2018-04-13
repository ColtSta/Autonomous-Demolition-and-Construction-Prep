import RPi.GPIO as GPIO
import time
from time import sleep
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

leftWheelF = 16
leftWheelR = 21
rightWheelF = 17
rightWheelR = 27
loaderU = 24
loaderD = 23


def init_motors():

	GPIO.setup(leftWheelF,GPIO.OUT)
	GPIO.setup(leftWheelR,GPIO.OUT)
	GPIO.setup(rightWheelF,GPIO.OUT)
	GPIO.setup(rightWheelR,GPIO.OUT)
	GPIO.setup(loaderU,GPIO.OUT)
	GPIO.setup(loaderD,GPIO.OUT)
	global lwf
	global rwf
	global lwr
	global rwr 
	lwf = GPIO.PWM(leftWheelF, 500)
	lwr = GPIO.PWM(leftWheelR, 500)
	rwf = GPIO.PWM(rightWheelF, 500)
	rwr = GPIO.PWM(rightWheelR, 500)

def forward():

	GPIO.output(leftWheelF,GPIO.HIGH)
	GPIO.output(rightWheelF,GPIO.HIGH)
	time.sleep(.2)
	print("forward")
	GPIO.output(leftWheelF,GPIO.LOW)
	GPIO.output(rightWheelF,GPIO.LOW)

def reverse():

	GPIO.output(leftWheelR,GPIO.HIGH)
        GPIO.output(rightWheelR,GPIO.HIGH)
        time.sleep(.2)
	print("reverse")
        GPIO.output(leftWheelR,GPIO.LOW)
        GPIO.output(rightWheelR,GPIO.LOW)

def left(angle):
	print("Turn left")
	GPIO.output(leftWheelR,GPIO.HIGH)
	GPIO.output(rightWheelF,GPIO.HIGH)
	time.sleep(.5)
	stop()

def right(angle):
	print("Turn right")
	GPIO.output(leftWheelF,GPIO.HIGH)
	GPIO.output(rightWheelR,GPIO.HIGH)
	time.sleep(.5)
	stop()

def stop():
	print("Stop")
	lwf.stop()
	lwr.stop()
	rwf.stop()
	rwr.stop()
	GPIO.output(leftWheelF,GPIO.LOW)
	GPIO.output(leftWheelR,GPIO.LOW)
	GPIO.output(rightWheelF,GPIO.LOW)
	GPIO.output(rightWheelR,GPIO.LOW)
	GPIO.output(loaderU,GPIO.LOW)
	GPIO.output(loaderD,GPIO.LOW)
