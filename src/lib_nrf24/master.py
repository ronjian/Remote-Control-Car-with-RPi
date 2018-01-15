import RPi.GPIO as GPIO
from lib_nrf24 import NRF24
import time
import spidev

GPIO.setmode(GPIO.BCM)
pipes = [[0xe7, 0xe7, 0xe7, 0xe7, 0xe7], [0xc2, 0xc2, 0xc2, 0xc2, 0xc2]]

radio = NRF24(GPIO, spidev.SpiDev())
radio.begin(0, 17)

radio.setRetries(15,15)
radio.setPayloadSize(32)
radio.setChannel(0x60)
radio.setDataRate(NRF24.BR_2MBPS)
radio.setPALevel(NRF24.PA_MIN)
radio.setAutoAck(True)
radio.enableDynamicPayloads()
radio.enableAckPayload()

radio.openWritingPipe(pipes[1])
radio.openReadingPipe(1, pipes[0])
radio.printDetails()

ackPL = [1]

def receiveData():
    print("Ready to receive data.")
    radio.startListening()
    pipe = [0]
    while not radio.available(pipe):
        time.sleep(1/100)
    receivedMessage = []
    radio.read(receivedMessage, radio.getDynamicPayloadSize())

    print("Translating the receivedMessage to unicode characters...")
    string = ""
    for n in receivedMessage:
        # We want to only decode standard symbols/alphabet/numerals
        # Based off unicode standards, our encoding method
        if (n >= 32 and n <= 126):
            string += chr(n)
    print("Our sensor sent us: {}".format(string))
    radio.stopListening()

while True:
    command = "GET_TEMP"
    message = []
    message = list(command)

    # send a packet to receiver
    radio.write(message)
    print("Sent: {}".format(message))

    # did it return with a payload?
    if radio.isAckPayloadAvailable():
        pl_buffer=[]
        radio.read(pl_buffer, radio.getDynamicPayloadSize())
        print(pl_buffer)
        print("Translating the acknowledgement to unicode characters...")
        string = ""
        for n in pl_buffer:
            # We want to only decode standard symbols/alphabet/numerals
            # Based off unicode standards, our encoding method
            if (n >= 32 and n <= 126):
                string += chr(n)
        print(string)
        # So our command was received and acknowledged. We should
        # setup ourselves to receive what that temperature was.
        receiveData()
    else:
        print("No received acknowledgement.")
    time.sleep(0.5)