import serial
import time
from config import ConfigTF

config = ConfigTF()

address = config.get_config("buzzer_serial_address")

ser = serial.Serial(adress, 9600)
time.sleep(2)

def buzzer_on():

	ser.write(b'on')
