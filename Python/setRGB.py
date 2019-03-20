from Utility import *

#load  Serial Port
arduino, port = serialAVR()
maxB = config['maxBrightness']
anzahl = int(input("Anzahl Farbakzente: "))
colors = list()

#begin data with a delimiter.
data = delimiter()

if anzahl > 1:
	ps = input("gib die prozentuale verteilung an: ")
	ps = [float(p) for p in ps.split(' ')]
	minP = ps.index(min(ps))

	for i in range(anzahl):
		c = input("Farbwerte (0-1) R G B: ")
		r, g, b = c.split(' ')
		r = int(maxB * float(r))
		g = int(maxB * float(g))
		b = int(maxB * float(b))
		colors.append([r, g, b])
	complement = colors[0]

else:
#read RGB from Console
	r = int(maxB * float(input("Rot (0-1): ")))
	g = int(maxB * float(input("Grün (0-1): ")))
	b = int(maxB * float(input("Blau (0-1): ")))
	colors.append([r, g, b])


	# build Complement
	h,s,v = rgb2hsv(colors[0])
	h = (h + 0.5) % 1
	complement = hsv2rgb(h, s, v)

data = rgb2bytes(complement)

ledsLeft = config['leds']
for i in range(anzahl-1):
	leds = int(round(ps[i] * config['leds'], 0))
	ledsLeft -= leds
	data += leds.to_bytes(2, byteorder='big') + rgb2bytes(colors[i])
data += ledsLeft.to_bytes(2, byteorder='big') + rgb2bytes(colors[anzahl-1])
sent = arduino.write(data)

#Debug
if printOutBufferSize:
    if arduino.out_waiting > 0:
        print(arduino.out_waiting)

if printComplement:
	print(complement)
	
if printOutData:
    print('Bytes sent:', sent, 'Bytes to send:', len(data), 'Data:', data.hex())