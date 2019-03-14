import sys
import glob
import serial
import colorsys
import json
from itertools import groupby

configFile = json.loads(open('config.json').read())
config = configFile['config']
debug = configFile['debug']
scale = config['maxBrightness'] / 255

printComplement = 'printComplement' in debug and debug['printComplement']
printDataRate = 'printDataRate' in debug and debug['printDataRate']
printInData = 'printInData' in debug and debug['printInData']
printOutData = 'printOutData' in debug and debug['printOutData']




def serial_ports():
    """ Lists serial port names

        :raises EnvironmentError:
            On unsupported or unknown platforms
        :returns:
            A list of the serial ports available on the system
    """
    if sys.platform.startswith('win'):
        ports = ['COM%s' % (i + 1) for i in range(256)]
    elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
        # this excludes your current terminal "/dev/tty"
        ports = glob.glob('/dev/tty[A-Za-z]*')
    elif sys.platform.startswith('darwin'):
        ports = glob.glob('/dev/tty.*')
    else:
        raise EnvironmentError('Unsupported platform')

    result = []
    for port in ports:
        try:
            s = serial.Serial(port)
            s.close()
            result.append(port)
        except (OSError, serial.SerialException):
            pass
    return result




def serialAVR():
    if 'port' in config:
        port = config['port']
    else:
        ports = serial_ports()
        if len(ports) > 1:
            port = ports[len(ports)-1]
        else:
            port = ports[0]
    # open Serial Port
    try:
        arduino = serial.Serial(port)
    except Exception:
        print("Can't open Port, check Config or Connection")
        input()
        exit()
    arduino.baudrate = 115200
    return arduino, port




def rgb2hsv(l : list):
    return colorsys.rgb_to_hsv(l[0]/255, l[1]/255, l[2]/255)




def hsv2rgb(h,s,v):
    return tuple(round(i * 255) for i in colorsys.hsv_to_rgb(h,s,v))




def rgb2bytes(rgb):
    return rgb[0].to_bytes(1, byteorder='big') + rgb[1].to_bytes(1, byteorder='big') + rgb[2].to_bytes(1, byteorder='big')

def delimiter():
    #zero = 0.to_bytes(1, byteorder='big')
    #ff = 255.to_bytes(1, byteorder='big')
    #return zero + zero + zero + zero + zero + zero + ff
    rg = [0,255]
    return rg[0].to_bytes(1, byteorder='big')+rg[0].to_bytes(1, byteorder='big')+rg[0].to_bytes(1, byteorder='big')+rg[0].to_bytes(1, byteorder='big')+rg[0].to_bytes(1, byteorder='big')+rg[0].to_bytes(1, byteorder='big') + rg[1].to_bytes(1, byteorder='big')

def RLE(byte, rescale=False):
    out = b''
    bytelist = list()
    maxCount = 0
    maxList = list()
    for i in range(0, len(byte), 3):
        bytelist.append(list(byte[i:i+3]))

    for key, group in groupby(bytelist):
        grplstlen = len(list(group))
        if grplstlen > maxCount:
            maxCount = grplstlen
            if rescale:
                maxList = [int(i*scale) for i in key]
            else:
                maxList = [int(round(i*255)) for i in key]
        out += grplstlen.to_bytes(config['counterSize'], byteorder='big')
        for i in key:
            if rescale:
                i = int(round(i*scale))
            out += i.to_bytes(1, byteorder='big')
    return out,  maxList

def deRLE(bytes):
    print(bytes)
    print("Komplement:", [bytes[0], bytes[1], bytes[2]])

    for i in range(0, len(bytes[3:]), 5):
        c = int.from_bytes(bytes[i:i+2], byteorder='big')
        r = bytes[i+3]
        g = bytes[i+4]
        b = int.from_bytes(bytes[i+3:i+4], byteorder='big')

        print("Anzahl:", c, "- RGB:", r, g, b)


if __name__ == '__main__':
    print(serial_ports())
    input()