import serial
import time
from socket import *
import colorsys
import json
from Utility import *

def main():
    #load  Serial Port
    arduino, port = serialAVR()

    # open Socket
    serverSocket = socket(AF_INET, SOCK_DGRAM)
    serverSocket.bind(('', config['socketport']))

    inCounter = 0
    outCounter = 0
    start = time.time()
    print("Piping to ", port, " ...")
    while True:
        sent = 0
        #Get Data
        message, addresse = serverSocket.recvfrom(1487)

        #RLE
        rle, maxColor = RLE(message, rescale=True)

        # build Complement
        h, s, v = rgb2hsv(maxColor)
        h =  (h + 0.5) % 1 # Colorshift by 180° in percent
        complement = hsv2rgb(h, s, v)
        complementbytes = rgb2bytes(complement)

        #Send Data
        sent += arduino.write(complement)
        sent += arduino.write(rle)

        #Debug Outputs
        if printOutBufferSize:
            if arduino.out_waiting > 0:
                print(arduino.out_waiting)

        if printComplement:
            print('Complement to main accent:', complement)

        if printInData:
            print('Bytes received:', len(message), 'Data:', message.hex())

        if printOutData:
            print('Bytes sent:', sent, 'Bytes to send:', len(rle), 'Data:', rle.hex())

        if printOutDataRate:
            inCounter += len(rle)
            print('Average:', int(round(inCounter / (time.time() - start), 0)), 'B/s')

        if printOutDataRate:
            outCounter += len(rle)
            print('Average:', int(round(outCounter / (time.time() - start), 0)), 'B/s')

if __name__  == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        exit()
