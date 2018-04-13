import RPi.GPIO as GPIO
import time
import lib_fl as fl
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)


fl.init_motors()
fl.stop()
while True:
	command = raw_input("Direction: ")
	if command == 'w':
		GPIO.output(fl.leftWheelF,GPIO.HIGH)
		GPIO.output(fl.rightWheelF,GPIO.HIGH)
		time.sleep(.5)
		GPIO.output(fl.leftWheelF,GPIO.LOW)
		GPIO.output(fl.rightWheelF,GPIO.LOW)
	elif command == 'a':
		for i in range(0,2):
			GPIO.output(fl.leftWheelR,GPIO.HIGH)
			GPIO.output(fl.rightWheelF,GPIO.HIGH)
			time.sleep(.1)
			GPIO.output(fl.leftWheelR,GPIO.LOW)
			GPIO.output(fl.rightWheelF,GPIO.LOW)
	elif command == 'd':
		for i in range(0,2):
			GPIO.output(fl.rightWheelR,GPIO.HIGH)
			GPIO.output(fl.leftWheelF,GPIO.HIGH)
			time.sleep(.1)
			GPIO.output(fl.rightWheelR,GPIO.LOW)
			GPIO.output(fl.leftWheelF,GPIO.LOW)
	elif command == 'r':
		GPIO.output(fl.loaderU,GPIO.HIGH)
		time.sleep(.7)
		GPIO.output(fl.loaderU,GPIO.LOW)
	elif command == 'f':
		GPIO.output(fl.loaderD,GPIO.HIGH)
		time.sleep(.7)
		GPIO.output(fl.loaderD,GPIO.LOW)
	#	fl.lwr.start(50)
#		fl.rwf.start(90)
#		time.sleep(.5)
#		fl.lwr.stop()
#		fl.rwf.stop()
#		time.sleep(.5)
#		fl.rwf.start(90)
#		time.sleep(.1)
#		fl.rwf.stop()
	elif command == 's':
		GPIO.output(fl.leftWheelR,GPIO.HIGH)
		GPIO.output(fl.rightWheelR,GPIO.HIGH)
		time.sleep(.5)
		GPIO.output(fl.leftWheelR,GPIO.LOW)
		GPIO.output(fl.rightWheelR,GPIO.LOW)
	elif command == '1':
		GPIO.output(fl.leftWheelF,GPIO.HIGH)
		time.sleep(.5)
		GPIO.output(fl.leftWheelF,GPIO.LOW)
	elif command == '2':
		GPIO.output(fl.rightWheelF,GPIO.HIGH)
		time.sleep(.5)
		GPIO.output(fl.rightWheelF,GPIO.LOW)
	elif command == '3':
		GPIO.output(fl.leftWheelR,GPIO.HIGH)
		time.sleep(.5)
		GPIO.output(fl.leftWheelR,GPIO.LOW)
	elif command == '4':
		GPIO.output(fl.rightWheelR,GPIO.HIGH)
		time.sleep(1)
		GPIO.output(fl.rightWheelR,GPIO.LOW)
	elif command == 'u':
		GPIO.output(fl.loaderU,GPIO.HIGH)
		time.sleep(1)
		GPIO.output(fl.loaderU,GPIO.LOW)
	elif command == 'j':
		GPIO.output(fl.loaderD,GPIO.HIGH)
		time.sleep(1)
		GPIO.output(fl.loaderD,GPIO.LOW)
	else:
		break
