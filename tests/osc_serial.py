import serial
import sliplib
from pythonosc.osc_message import OscMessage
import time

# Serial port configuration
SERIAL_PORT = '/dev/cu.usbmodem14601'  # Update this with your serial port
BAUD_RATE = 1000000              # Update this with your baud rate

ser = serial.Serial(SERIAL_PORT, BAUD_RATE)
t = 0
try:
    buffer = bytearray()
    while True:
        byte = ser.read()

        if byte == sliplib.END:
            
            if len(buffer) > 0:

                osc_message = OscMessage(buffer)
                print("Received OSC message:", osc_message.address, osc_message.params, "at", round(time.time()-t, 2), "seconds")
                buffer.clear()
                t = time.time()
        else:
            buffer.append(byte[0])

except KeyboardInterrupt:
    ser.close()
    print("Serial connection closed.")