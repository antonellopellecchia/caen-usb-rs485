#!/usr/bin/python3

import sys
import serial
import argparse

def read_result(ser):
    result = b''
    c = b''
    while c!=b'\n':
        c = ser.read()
        result += c
    return result

parser = argparse.ArgumentParser()
parser.add_argument("port", type=str, help="Serial port to read")
parser.add_argument("command", type=str, help="MON or SET")
parser.add_argument("channel", type=int, help="HV channel number")
parser.add_argument("voltage", type=float, nargs='?', help="Voltage to set")
args = parser.parse_args()

ser = serial.Serial(args.port, 9600, parity=serial.PARITY_NONE)
#ser.set_input_flow_control(True)
ser.xonxoff = True
print('Connection settings:')
settings = ser.get_settings()
for key in settings: print(f'{key}: {settings[key]}')
print()

if args.command=='SET':
    command = f'$BD:00,CMD:SET,CH:{args.channel},PAR:VSET,VAL:{args.voltage}\r\n'.encode()
elif args.command=='MON':
    command = f'$BD:00,CMD:MON,CH:{args.channel},PAR:VSET\r\n'.encode()
else:
    print('Unrecognized command')
    sys.exit(1)

print('Sending command:', command)
ser.write(command)
print('Response:', read_result(ser))
