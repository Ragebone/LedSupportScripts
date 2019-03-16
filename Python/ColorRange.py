from Utility import *
import time

arduino, port = serialAVR()
leds = config['leds']
maxB = config['maxBrightness'] / 255
steps = int(input("Wie viele Schritte: "))
stepSize = 1/steps

l = 0
s = 1
block = stepSize * leds
out = rgb2bytes([0, 0, 0])
i = 0
for i in range(steps - 1):
	out += int(block).to_bytes(2, byteorder='big') + rgb2bytes(hsv2rgb(i * stepSize, s, maxB))

out += int(leds - i * block).to_bytes(2, byteorder='big') + rgb2bytes(hsv2rgb((i+1) * stepSize, s, maxB))

deRLE(out)
