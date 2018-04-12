import RPi.GPIO as GPIO
import time, sys, tty, termios
from time import sleep
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

leftTrackF = 27
leftTrackR = 18
rightTrackR = 19
rightTrackF = 25
boomUp = 26
boomDn = 13
stickEx = 16
stickRt = 20
bucketUp = 12
bucketDn = 21
turnL = 22
turnR = 17

def init_motors():

	GPIO.setup(leftTrackF,GPIO.OUT)
	GPIO.setup(leftTrackR,GPIO.OUT)
	GPIO.setup(rightTrackF,GPIO.OUT)
	GPIO.setup(rightTrackR,GPIO.OUT)
	GPIO.setup(boomUp,GPIO.OUT)
	GPIO.setup(boomDn,GPIO.OUT)
	GPIO.setup(stickEx,GPIO.OUT)
	GPIO.setup(stickRt,GPIO.OUT)
	GPIO.setup(bucketUp,GPIO.OUT)
	GPIO.setup(bucketDn,GPIO.OUT)
	GPIO.setup(turnL,GPIO.OUT)
	GPIO.setup(turnR,GPIO.OUT)

def turnLeft(angle):
	GPIO.output(leftTrackR,GPIO.HIGH)
	GPIO.output(rightTrackF,GPIO.HIGH)
	time.sleep(2.3)
	GPIO.output(leftTrackR,GPIO.LOW)
	GPIO.output(rightTrackF,GPIO.LOW)
	print("turned left")

def turnRight(angle):
        GPIO.output(leftTrackF,GPIO.HIGH)
        GPIO.output(rightTrackR,GPIO.HIGH)
        time.sleep(2)
        GPIO.output(leftTrackF,GPIO.LOW)
        GPIO.output(rightTrackR,GPIO.LOW)
	print("turned right")

def forward():

	GPIO.output(leftTrackR,GPIO.HIGH)
	GPIO.output(rightTrackR,GPIO.HIGH)
	time.sleep(1)
  	GPIO.output(leftTrackR,GPIO.LOW)
        GPIO.output(rightTrackR,GPIO.LOW)
	print("forward")

def reverse():

	GPIO.output(leftTrackF,GPIO.HIGH)
        GPIO.output(rightTrackF,GPIO.HIGH)
        time.sleep(1)
	GPIO.output(leftTrackF,GPIO.LOW)
        GPIO.output(rightTrackF,GPIO.LOW)
	print("reverse")

def rotateLeft():
	GPIO.output(turnL,GPIO.HIGH)
	time.sleep(2.2)
	GPIO.output(turnL,GPIO.LOW)
	print("rotate Left")

def rotateRight():
	GPIO.output(turnR,GPIO.HIGH)
	time.sleep(2.2)
	GPIO.output(turnR,GPIO.LOW)
	print("Rotate Right")

def bmUp():
	GPIO.output(boomUp,GPIO.HIGH)
	time.sleep(1)
	GPIO.output(boomUp,GPIO.LOW)
	print("boom up")

def bmDn():
	GPIO.output(boomDn,GPIO.HIGH)
	time.sleep(1)
	GPIO.output(boomDn,GPIO.LOW)
	print("boom down")

def stkEx():
	GPIO.output(stickEx,GPIO.HIGH)
	time.sleep(1)
	GPIO.output(stickEx,GPIO.LOW)
	print("Stick Extend")

def stkRt():
	GPIO.output(stickRt,GPIO.HIGH)
	time.sleep(1)
	GPIO.output(stickRt,GPIO.LOW)
	print("stick retract")

def bktUp():
	GPIO.output(bucketUp,GPIO.HIGH)
	time.sleep(1)
	GPIO.output(bucketUp,GPIO.LOW)
	print("bucket up")

def bktDn():
	GPIO.output(bucketDn,GPIO.HIGH)
	time.sleep(1)
	GPIO.output(bucketDn,GPIO.LOW)
	print("bucket down")


def dig ():
	rotateLeft()
	GPIO.output(stickEx, GPIO.HIGH)
	GPIO.output(bucketDn, GPIO.HIGH)
	time.sleep(1)
	GPIO.output(stickEx, GPIO.LOW)
	GPIO.output(bucketDn, GPIO.LOW)

	GPIO.output(stickEx,GPIO.HIGH)
	time.sleep(2)
	GPIO.output(stickEx,GPIO.LOW)

	GPIO.output(boomDn,GPIO.HIGH)
	time.sleep(1.25)
	GPIO.output(boomDn,GPIO.LOW)

	GPIO.output(bucketUp, GPIO.HIGH)
        time.sleep(.3)
        GPIO.output(bucketUp, GPIO.LOW)

#	GPIO.output(boomDn, GPIO.HIGH)
#	time.sleep(.1)
#	GPIO.output(boomDn, GPIO.LOW)

	GPIO.output(stickRt, GPIO.HIGH)
	time.sleep(2.2)
	GPIO.output(stickRt,GPIO.LOW)

	GPIO.output(bucketUp, GPIO.HIGH)
	time.sleep(.8)
	GPIO.output(bucketUp, GPIO.LOW)

	GPIO.output(boomUp, GPIO.HIGH)
	GPIO.output(stickRt, GPIO.HIGH)
	GPIO.output(bucketUp, GPIO.HIGH)
	time.sleep(.3)
	GPIO.output(bucketUp, GPIO.LOW)
	GPIO.output(stickRt, GPIO.LOW)
	time.sleep(2.7)
	GPIO.output(boomUp, GPIO.LOW)

	rotateRight()
	stop()

	print("dig")
def dig2():
	rotateLeft()
        GPIO.output(stickEx, GPIO.HIGH)
        GPIO.output(bucketDn, GPIO.HIGH)
        time.sleep(1)
        GPIO.output(stickEx, GPIO.LOW)
        GPIO.output(bucketDn, GPIO.LOW)

        GPIO.output(stickEx,GPIO.HIGH)
        time.sleep(2)
        GPIO.output(stickEx,GPIO.LOW)


	GPIO.output(boomDn,GPIO.HIGH)
        time.sleep(1.4)
        GPIO.output(boomDn,GPIO.LOW)

        GPIO.output(bucketUp, GPIO.HIGH)
        time.sleep(.3)
        GPIO.output(bucketUp, GPIO.LOW)

#       GPIO.output(boomDn, GPIO.HIGH)
#       time.sleep(.1)
#       GPIO.output(boomDn, GPIO.LOW)

        GPIO.output(stickRt, GPIO.HIGH)
        time.sleep(2.2)
        GPIO.output(stickRt,GPIO.LOW)

        GPIO.output(bucketUp, GPIO.HIGH)
        time.sleep(.8)
        GPIO.output(bucketUp, GPIO.LOW)

        GPIO.output(boomUp, GPIO.HIGH)
        GPIO.output(stickRt, GPIO.HIGH)
        GPIO.output(bucketUp, GPIO.HIGH)
        time.sleep(.3)
        GPIO.output(bucketUp, GPIO.LOW)
        GPIO.output(stickRt, GPIO.LOW)
        time.sleep(2.7)
        GPIO.output(boomUp, GPIO.LOW)

        rotateRight()
        stop()


def dump():
	rotateRight()

	GPIO.output(stickEx,GPIO.HIGH)
	GPIO.output(bucketDn, GPIO.HIGH)
	time.sleep(1)
	GPIO.output(stickEx, GPIO.LOW)
	GPIO.output(bucketDn, GPIO.LOW)

	GPIO.output(boomDn,GPIO.HIGH)
	time.sleep(.1)
	stop()

	stkRt()
	bktUp()
	rotateLeft()
#	GPIO.output(turnL, GPIO.HIGH)
#	time.sleep(1.2)
#	GPIO.output(turnL, GPIO.LOW)
	stop()


def stop():
	print("Stop")
	GPIO.output(leftTrackF,GPIO.LOW)
	GPIO.output(leftTrackR,GPIO.LOW)
	GPIO.output(rightTrackF,GPIO.LOW)
	GPIO.output(rightTrackR,GPIO.LOW)
	GPIO.output(turnL,GPIO.LOW)
	GPIO.output(turnR,GPIO.LOW)
	GPIO.output(boomUp,GPIO.LOW)
	GPIO.output(boomDn,GPIO.LOW)
	GPIO.output(stickEx,GPIO.LOW)
	GPIO.output(stickRt,GPIO.LOW)
	GPIO.output(bucketUp,GPIO.LOW)
	GPIO.output(bucketDn,GPIO.LOW)
