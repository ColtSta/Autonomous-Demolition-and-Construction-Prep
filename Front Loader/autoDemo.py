
import RPi.GPIO as GPIO
from lib_nrf24 import NRF24
import time
import spidev
import lib_fl as fl
import math

def callback(data):
	print("Interrupted")
	receivedMessage = []
        radio.read(receivedMessage, radio.getDynamicPayloadSize())
        string = ""
        for n in receivedMessage:
                if (n >= 32 and n <= 126):
                        string += chr(n)
	global xLoc
	global yLoc
	global xGoal
	global yGoal
	global ready
	global newTask
	if string[1] == 'f':
		ready = True
		xLoc = int(string[5])
		yLoc = int(string[6])
		xGoal = int(string[7])
		yGoal = int(string[8])
		newTask = True
	radio.stopListening()
	radio.startListening()

ready = False

GPIO.setmode(GPIO.BCM)
GPIO.setup(26,GPIO.IN)
GPIO.add_event_detect(26,GPIO.BOTH,callback=callback,bouncetime = 30)
pipes = [[0xE8, 0xE8, 0xF0, 0xF0, 0xE1], [0xF0, 0xF0, 0xF0, 0xF0, 0xE1]]

radio = NRF24(GPIO, spidev.SpiDev())
radio.begin(0,4)

radio.setPayloadSize(32)
radio.setChannel(0x76)
radio.setDataRate(NRF24.BR_1MBPS)
radio.setPALevel(NRF24.PA_MIN)

radio.setAutoAck(True)
radio.enableDynamicPayloads()
radio.enableAckPayload()

radio.openReadingPipe(1, pipes[1])
radio.printDetails()
radio.startListening()

fl.init_motors()

print("Waiting for initial data")
while not ready:
	time.sleep(1/100)

newTask = True
needAngle = True

while True:
	if newTask and needAngle:
		angle = int(math.degrees(math.atan2((yGoal - yLoc),(xGoal-xLoc))))
		distance = math.sqrt(((yGoal-yLoc)**2)+(xGoal-xLoc)**2)
		needAngle = False
		print("Angle: {}".format(angle))
		print("Distance: {}".format(distance))
		if angle > 0:
			fl.left(abs(angle))
			fl.stop()
			time.sleep(.5)
		else:
			fl.right(abs(angle))
			fl.stop()
		newTask = False
		time.sleep(1)
		print("tried turning")
	#print("xLoc: {} yLoc: {} xGoal: {} yGoal: {}".format(xLoc,yLoc,xGoal,yGoal))

	if xLoc != xGoal and yLoc != yGoal:
		fl.forward(100)
		time.sleep(.1)
		fl.stop()
	elif xLoc == xGoal and yLoc == yGoal:
		print("Made it")
		print("xLoc: {} yLoc: {} xGoal: {} yGoal: {}".format(xLoc, yLoc, xGoal, yGoal))
		print("Waiting for new task")
		while not newTask:
			time.sleep(1/100)
		needAngle = True


