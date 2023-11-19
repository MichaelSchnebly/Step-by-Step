import serial
from pythonosc import osc_message_builder
from pythonosc import osc_bundle_builder
from pythonosc import osc_packet
import time

# Set up serial connection (adjust the COM port as needed)
serial_port = '/dev/ttyUSB0'  # Example for Linux
baud_rate = 115200
ser = serial.Serial(serial_port, baud_rate)

while True:
    # Read from serial port
    if ser.in_waiting > 0:
        serial_data = ser.readline().decode('utf-8').strip()

        # Parse the OSC message
        try:
            # OSC messages are typically binary, so you may need to adjust this
            osc_msg = osc_packet.OscPacket(serial_data).messages
            print("Received OSC message:", osc_msg)
        except Exception as e:
            print("Error parsing OSC message:", e)

        # Add a small delay to avoid high CPU usage
        time.sleep(0.1)