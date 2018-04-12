import RPi.GPIO as GPIO
import time
from time import sleep
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

leftWheelF = 26 #pin37
leftWheelR = 20 #pin38
rightWheelF = 19 #pin35
rightWheelR = 16 #pin33
dump = 21 #pin40


def init_motors():

	GPIO.setup(leftWheelF,GPIO.OUT)
	GPIO.setup(leftWheelR,GPIO.OUT)
	GPIO.setup(rightWheelF,GPIO.OUT)
	GPIO.setup(rightWheelR,GPIO.OUT)
	GPIO.setup(21,GPIO.OUT)
	global lwf
	global rwf
	global lwr
	global rwr 
	lwf = GPIO.PWM(leftWheelF, 50)
	lwr = GPIO.PWM(leftWheelR, 50)
	rwf = GPIO.PWM(rightWheelF, 50)
	rwr = GPIO.PWM(rightWheelR, 50)

def forward():

	GPIO.output(rightWheelF,GPIO.HIGH)
	GPIO.output(leftWheelF,GPIO.HIGH)
#	lwf.start(speed)
#	rwf.start(speed)
	time.sleep(2)
#	lwf.stop()
#	rwf.stop()
	GPIO.output(leftWheelF,GPIO.LOW)
	GPIO.output(rightWheelF,GPIO.LOW)

def reverse():

	GPIO.output(leftWheelR,GPIO.HIGH)
        GPIO.output(rightWheelR,GPIO.HIGH)
        time.sleep(2)
        GPIO.output(leftWheelR,GPIO.LOW)
        GPIO.output(rightWheelR,GPIO.LOW)

def stop():
	GPIO.output(leftWheelF,GPIO.LOW)
	GPIO.output(leftWheelR,GPIO.LOW)
	GPIO.output(rightWheelF,GPIO.LOW)
	GPIO.output(rightWheelR,GPIO.LOW)
	GPIO.output(21,GPIO.LOW)

def dump():
	GPIO.output(21, GPIO.HIGH)
	time.sleep(1.2)
	stop()
