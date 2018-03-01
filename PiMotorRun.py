import PiMotor
import time
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BOARD)

#def run():
'''Procedure to test all the motor pins

Outputs to the terminal which motor is being powered and which config is being executed.
Calls the "Forward" method in order to demonstrate which config you should be using to 
define the correct "forward" for your project.
'''
    #d = ["MOTOR1","MOTOR2","MOTOR3","MOTOR4"]
    #for motor in d:
        #for config in range(1,3):
     #       print(motor + " config: " + str(1))
     #       m1 = PiMotor.Motor("MOTOR1",1)
#	    m2 = PiMotor.Motor("MOTOR2",1)
#            m1.forward(100)
#	    m2.forward(100)

#            time.sleep(2)
#            m1.stop()
#	    m2.stop()
#try:
#    while True:
        # Continously test all the Motor's
#        run()

#except KeyboardInterrupt:
#    print("\nExiting Motor Shield Testing\n")
ab = PiMotor.Arrow(4)
af = PiMotor.Arrow(2)
al = PiMotor.Arrow(1)
ar = PiMotor.Arrow(3)  
m1 = PiMotor.Motor("MOTOR1",1)
m2 = PiMotor.Motor("MOTOR2",1)
m3 = PiMotor.Motor("MOTOR3",2)
m4 = PiMotor.Motor("MOTOR4",2)
mtrs = PiMotor.LinkedMotors(m1,m3)
#mtrs2 = PiMotor.LinkedMotors(m2,m4)
while 1:
	data = raw_input("direction:")
	if data == "w":
		af.on()
		mtrs.forward(100)
		time.sleep(1)
		af.off()
		mtrs.stop()

	elif data == "s":
		ab.on()
		mtrs.reverse(100)
		time.sleep(1)
		ab.off()
		mtrs.stop()

	elif data == "a":
		count = 4
		al.on()
		while count > 0:
			m1.reverse(100)
			m3.forward(100)
			time.sleep(.3)
			m1.stop()
			m3.stop()
			time.sleep(.1)
			m1.reverse(100)
			m3.reverse(100)
			time.sleep(.2)
			m3.stop()
			m1.stop()
			time.sleep(.1)
			m1.reverse(100)
			m3.forward(100)
			time.sleep(.3)
			m1.stop()
			m3.stop()
			time.sleep(.1)
			m1.forward(100)
			m3.forward(100)
			time.sleep(.2)
			m1.stop()
			m3.stop()
			count -= 1
		m1.stop()
		m3.stop()
		al.off()

	elif data == "d":
		ar.on()
		m1.forward(100)
		m3.reverse(100)
		time.sleep(1)
		ar.off()
		m1.stop()
		m3.stop()
	elif data == "f": #lower arm
		m4.reverse(100)
		m2.forward(100)
		af.on()
		ab.on()
		time.sleep(.5)
		af.off()
		ab.off()
		m2.stop()
		m4.stop()
	elif data == "r": #raise arm
		m2.reverse(100)
		m4.forward(100)
		al.on()
		ar.on()
		time.sleep(.5)
		al.off()
		ar.off()
		m4.stop()
		m2.stop()

	elif data == "1":
		m1.forward(100)
		m3.reverse(100)
		time.sleep(1)
		m1.stop()
		m3.stop()

	elif data == "2":
		m2.forward(100)
		time.sleep(1)
		m2.stop()

	elif data == "3":
		m3.forward(100)
		m1.reverse(100)
		time.sleep(1)
		m3.stop()
		m1.stop()

	elif data == "4":
		m4.forward(100)
		time.sleep(1)
		m4.stop()

	elif data == "`":
		mtrs.reverse(100)
		time.sleep(.2)
		mtrs.stop()
	else:
		break
