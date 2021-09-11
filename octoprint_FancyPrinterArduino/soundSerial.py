import serial.tools.list_ports
import serial
ports = serial.tools.list_ports.comports()
testport = ''
for port, desc, hwid in sorted(ports):
    print("{}: {} [{}]".format(port, desc, hwid))
    testport = port

ser = serial.Serial(testport, 115200)
ser.write('7\r\n'.encode())