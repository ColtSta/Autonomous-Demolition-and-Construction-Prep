import RPi.GPIO as GPIO
from lib_nrf24 import NRF24
import time
import spidev

def callback(data):
	GPIO.output(20,GPIO.HIGH)


GPIO.setmode(GPIO.BCM)
GPIO.setup(16,GPIO.IN)
GPIO.add_event_detect(16,GPIO.FALLING,callback)
pipes = [[0xE8, 0xE8, 0xF0, 0xF0, 0xE1], [0xF0, 0xF0, 0xF0, 0xF0, 0xE1]]

radio = NRF24(GPIO, spidev.SpiDev())
radio.begin(0,17)

radio.setPayloadSize(32)
radio.setChannel(0x66)
radio.setDataRate(NRF24.BR_1MBPS)
radio.setPALevel(NRF24.PA_MIN)

radio.setAutoAck(True)
radio.enableDynamicPayloads()
radio.enableAckPayload()

radio.openReadingPipe(1, pipes[1])
radio.printDetails()
radio.startListening()


while True:
	while not radio.available(0):
		time.sleep(1/100)
	
	receivedMessage = []
	radio.read(receivedMessage, radio.getDynamicPayloadSize())
	print("Received: {}".format(receivedMessage))

	print("Translating our received message into unicode characters...")
	string = ""

	for n in receivedMessage:
		if (n >= 32 and n <= 126):
			string += chr(n)
	if string == "Hello":
		print("noiice")
	print("Our received message decodes to: {}".format(string))

