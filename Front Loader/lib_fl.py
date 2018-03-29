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

def forward(speed):

	#GPIO.output(leftWheelF,GPIO.HIGH)
	#GPIO.output(rightWheelF,GPIO.HIGH)
	lwf.start(speed)
	rwf.start(speed)
	#time.sleep(1)
	print("forward")
	#lwf.stop()
	#rwf.stop()
	#time.sleep(.1)
	#GPIO.output(leftWheel1,GPIO.LOW)
	#GPIO.output(rightWheel1,GPIO.LOW)

def reverse(speed):

	#GPIO.output(leftWheel2,GPIO.HIGH)
        #GPIO.output(rightWheel2,GPIO.HIGH)
	lwr.start(speed)
	rwr.start(speed)
        #time.sleep(1)
	#lwr.stop()
	#rwr.stop()
       # GPIO.output(leftWheel2,GPIO.LOW)
       # GPIO.output(rightWheel2,GPIO.LOW)

def left(angle):
	print("Turn left")
	rwr.start(50)
	lwr.start(100)
	#GPIO.output(leftWheelR,GPIO.HIGH)
	#GPIO.output(rightWheelF,GPIO.HIGH)
	time.sleep(4*(angle/360))
	#time.sleep(1)
	#rwr.stop()
	#lwr.stop()
	#time.sleep(.1)
	#rwf.start(100)
	#lwf.start(50)
	#time.sleep(1)
	#rwf.stop()
	#lwf.stop()

def right(angle):
	print("Turn right")
	lwr.start(50)
        rwr.start(100)
        #time.sleep(1)
        #lwr.stop()
        #rwr.stop()
        #time.sleep(.1)
        #lwf.start(100)
        #rwf.start(50)
        #time.sleep(1)
        #lwf.stop()
        #rwf.stop()

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
	#GPIO.output(loaderU,GPIO.LOW)
	#GPIO.output(loaderD,GPIO.LOW)
