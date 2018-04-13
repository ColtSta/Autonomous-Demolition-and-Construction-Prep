

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
	print(string)
	global goals
	global xLoc
	global yLoc
	global xGoal
	global yGoal
	global ready
	global wait
	global angle
	if string[1] == 'f':
		if string[5] == 'g':
			goals = []
			for n in range(6,len(string)):
				if string[n] == '>':
					break
				else:
					goals.append(int(string[n]))

		elif string[5] == 'w':
			wait = True
			fl.stop()
		elif string[5] == 's':
			wait = False
			fl.stop()
		else:
			xLoc = int(string[5])
			yLoc = int(string[6])
			#xGoal = int(string[7])
			#yGoal = int(string[8])
			angle = int(math.degrees(math.atan2((goals[yGoalCount] - yLoc),(goals[xGoalCount] - xLoc))))
		#elif string[2] == 'w':
		#	wait = True
		#	fl.stop()
		#elif string[5] == 'g':
		#	fl.stop()
		#	wait = False
			ready = True
	radio.stopListening()
	radio.startListening()

ready = False
wait = False
# Set up interrupt pin
GPIO.setmode(GPIO.BCM)
GPIO.setup(26,GPIO.IN)
GPIO.add_event_detect(26,GPIO.BOTH,callback=callback,bouncetime = 30)

# Set up radio
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

# initialize motors
fl.init_motors()
angle = 0
xGoalCount = 0
yGoalCount = 1

print("Waiting for initial data")
while not ready:
	time.sleep(1/100)
print goals
newGoal = True
xLoc = 0
yLoc = 2
#angle = 0
xGoalReached = False
yGoalReached = False


while True:
	xGoal = goals[xGoalCount]
	yGoal = goals[yGoalCount]
	print("Current Goal {},{}".format(xGoal,yGoal))
	if newGoal and not wait:
		prevAngle = angle
		print("Angle: {}".format(prevAngle))
		#print("Distance: {}".format(distance))
		if prevAngle > 0 and prevAngle != 180:
			fl.left(abs(90))
			fl.stop()
		elif prevAngle < 0:
			fl.right(abs(90))
			fl.stop()
		elif prevAngle == 180:
			fl.reverse()
		newGoal = False
		time.sleep(1)

	while not yGoalReached and not wait:
		if yLoc != yGoal:
			fl.forward()
		elif yLoc == yGoal:
			fl.stop()
			if (prevAngle > 0 and prevAngle < 90) or (prevAngle < 0 and prevAngle > -90):
				fl.right(90)
			elif angle > 90 and angle < 180:
				fl.left(90)
			yGoalReached = True
			print("Y Goal Reached")

	yGoalReached = False

	while not xGoalReached and not wait:
		if xLoc != xGoal:
			print("X Location: {} X Goal: {}".format(xLoc,xGoal))
			fl.forward()
		elif xLoc == xGoal:
			fl.stop()
			xGoalReached = True
			print("X Goal Reached")

			if prevAngle == 90:
				fl.right(90)
			elif prevAngle == 90:
				fl.left(90)

	xGoalReached = False
	newGoal = True
	while wait:
		time.sleep(1/100)
	xGoalCount += 2
	yGoalCount += 2
