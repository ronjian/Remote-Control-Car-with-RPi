import RPi.GPIO as GPIO
from lib_nrf24 import NRF24
import time
import spidev

GPIO.setmode(GPIO.BCM)

pipes = [[0xe7, 0xe7, 0xe7, 0xe7, 0xe7], [0xc2, 0xc2, 0xc2, 0xc2, 0xc2]]

radio = NRF24(GPIO, spidev.SpiDev())
radio.begin(0, 17)
radio.setPayloadSize(32)
radio.setChannel(0x60)

radio.setDataRate(NRF24.BR_2MBPS)
radio.setPALevel(NRF24.PA_MIN)
radio.setAutoAck(True)
radio.enableDynamicPayloads()
radio.enableAckPayload()

radio.openWritingPipe(pipes[0])
radio.openReadingPipe(1, pipes[1])
radio.printDetails()

radio.startListening()

def getTemp():
    temp = 25
    return str(temp)

def sendData(ID, value):
    radio.stopListening()
    time.sleep(0.25)
    message = list(ID) + list(value)
    print("About to send the message.")
    radio.write(message)
    print("Sent the data.")
    radio.startListening()

while True:
    ackPL = [1]
    radio.writeAckPayload(1, ackPL, len(ackPL))
    while not radio.available(0):
        time.sleep(1/100)

    receivedMessage = []
    radio.read(receivedMessage, radio.getDynamicPayloadSize())
    print("Received: {}".format(receivedMessage))

    print("Translating the receivedMessage into unicode characters...")
    string = ""
    for n in receivedMessage:
        # Decode into standard unicode set
        if (n >=32 and n <= 126):
            string += chr(n)
    print(string)

    # We want to react to the command from the master.
    command = string
    if command == "GET_TEMP":
        print("We should get the temperature!")
        tempID = "temp_"
        temp = getTemp()
        sendData(tempID, temp)
    command = ""

    radio.writeAckPayload(1, ackPL, len(ackPL))
    print("Loaded payload reply of {}".format(ackPL))