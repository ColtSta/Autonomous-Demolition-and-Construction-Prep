
import lib_ex as ex
import RPi.GPIO as GPIO
import time
from time import sleep
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

ex.init_motors()
ex.stop()

while True:
	command = raw_input("Motor test: ")
	if command == 'w':
		ex.forward()
	elif command =='s':
		ex.reverse()
	elif command =='q':
		ex.rotateLeft()
	elif command =='e':
		ex.rotateRight()
	elif command =='t':
		ex.bmUp()
	elif command =='g':
		ex.bmDn()
	elif command =='y':
		ex.stkEx()
	elif command =='h':
		ex.stkRt()
	elif command =='u':
		ex.bktUp()
	elif command =='j':
		ex.bktDn()
	elif command =='d':
		ex.turnRight()
	elif command =='a':
		ex.turnLeft()
	elif command =='x':
		ex.dig()
		ex.dump()
	elif command =='v':
		ex.dig2()
		ex.dump()
	elif command =='c':
		ex.dump()
	else:
		ex.stop()


